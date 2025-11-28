"""Authentication endpoints."""

from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
import secrets

from app.db.session import get_db
from app.schemas.auth import LoginRequest, SignupRequest, Token
from app.schemas.user import UserResponse
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.deps import get_current_user
from app.core.settings import get_settings
from app.models.user import User

router = APIRouter()
settings = get_settings()

# Setup OAuth
oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@router.post("/login", response_model=Token)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """Login and get access token."""
    from sqlalchemy import select
    from app.models.user import User
    
    # Retrieve user by email
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()
    
    # Check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Verify password
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    # Create access token
    access_token = create_access_token(subject=str(user.id))
    
    return Token(access_token=access_token, token_type="bearer")


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignupRequest,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user and return access token."""
    from sqlalchemy import select
    from app.models.user import User
    
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == request.email))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="البريد الإلكتروني مسجل مسبقاً",
        )
    
    # Create new user
    hashed_password = get_password_hash(request.password)
    new_user = User(
        email=request.email,
        hashed_password=hashed_password,
        full_name=request.full_name,
        is_active=True,
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(subject=str(new_user.id))
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """Get current user information."""
    return current_user


@router.post("/refresh", response_model=Token)
async def refresh_token(
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token."""
    # TODO: Verify current token
    # TODO: Issue new token
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Token refresh not yet implemented",
    )


@router.get("/google/login")
async def google_login(request: Request):
    """Initiate Google OAuth login."""
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Handle Google OAuth callback."""
    try:
        # Get token from Google
        token = await oauth.google.authorize_access_token(request)
        
        # Get user info from Google
        user_info = token.get('userinfo')
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info from Google"
            )
        
        email = user_info.get('email')
        name = user_info.get('name', '')
        google_id = user_info.get('sub')
        
        if not email or not google_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or Google ID not provided"
            )
        
        # Check if user exists
        from sqlalchemy import select
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if not user:
            # Create new user
            user = User(
                email=email,
                full_name=name,
                hashed_password=get_password_hash(google_id),  # Use Google ID as password
                is_active=True,
                google_id=google_id
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        else:
            # Update Google ID if not set
            if not user.google_id:
                user.google_id = google_id
                await db.commit()
        
        # Create access token
        access_token = create_access_token(subject=str(user.id))
        
        # Redirect to frontend with token
        frontend_url = f"https://aidotoo.com/auth/callback?token={access_token}"
        return RedirectResponse(url=frontend_url)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Authentication failed: {str(e)}"
        )


# Password reset token storage (in production, use Redis or database)
password_reset_tokens = {}


async def send_password_reset_email(email: str, reset_token: str):
    """Send password reset email (mock implementation)."""
    # TODO: Implement actual email sending
    reset_link = f"https://aidotoo.com/reset-password?token={reset_token}"
    print(f"Password reset link for {email}: {reset_link}")
    # In production, use email service like SendGrid, AWS SES, etc.


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    request: dict,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Request password reset."""
    email = request.get("email")
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required"
        )
    
    # Check if user exists
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    
    # Always return success (security: don't reveal if email exists)
    if user:
        # Generate reset token
        reset_token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=1)
        
        # Store token (in production, use database)
        password_reset_tokens[reset_token] = {
            "email": email,
            "expires_at": expires_at
        }
        
        # Send email in background
        background_tasks.add_task(send_password_reset_email, email, reset_token)
    
    return {"message": "If the email exists, a reset link has been sent"}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    request: dict,
    db: AsyncSession = Depends(get_db),
):
    """Reset password with token."""
    token = request.get("token")
    new_password = request.get("new_password")
    
    if not token or not new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token and new password are required"
        )
    
    # Validate password length
    if len(new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )
    
    # Check if token exists and is valid
    token_data = password_reset_tokens.get(token)
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Check if token expired
    if datetime.utcnow() > token_data["expires_at"]:
        del password_reset_tokens[token]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired"
        )
    
    # Get user
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.email == token_data["email"]))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update password
    user.hashed_password = get_password_hash(new_password)
    await db.commit()
    
    # Delete used token
    del password_reset_tokens[token]
    
    return {"message": "Password has been reset successfully"}

