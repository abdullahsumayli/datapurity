"""Authentication schemas."""

from typing import Optional
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """JWT token payload."""

    sub: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema."""

    email: EmailStr
    password: str


class SignupRequest(BaseModel):
    """Signup request schema."""

    email: EmailStr
    password: str
    full_name: Optional[str] = None


class PasswordChange(BaseModel):
    """Password change request schema."""

    current_password: str
    new_password: str
