"""Test script for marketing funnel end-to-end flow."""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import text
from app.db.session import AsyncSessionLocal, engine
from app.schemas.lead import LeadCreate
from app.services.lead_service import create_lead


async def create_tables():
    """Create the leads table if it doesn't exist."""
    async with engine.begin() as conn:
        # Create leads table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(50),
                company VARCHAR(255),
                sector VARCHAR(100),
                source VARCHAR(50) NOT NULL DEFAULT 'landing_page',
                ip_address VARCHAR(45),
                user_agent VARCHAR(500),
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            )
        """))
        
        # Create index on email
        await conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email)
        """))
        
        print("✓ Leads table created successfully")


async def test_lead_creation():
    """Test creating a lead through the service layer."""
    async with AsyncSessionLocal() as db:
        # Test lead data
        lead_data = LeadCreate(
            full_name="أحمد محمد",
            email="ahmed@test.com",
            phone="+966501234567",
            company="شركة التقنية",
            sector="تقنية"
        )
        
        # Create lead
        lead = await create_lead(
            db=db,
            lead_data=lead_data,
            ip_address="127.0.0.1",
            user_agent="Test Script"
        )
        
        print(f"✓ Lead created successfully:")
        print(f"  ID: {lead.id}")
        print(f"  Name: {lead.full_name}")
        print(f"  Email: {lead.email}")
        print(f"  Phone: {lead.phone}")
        print(f"  Company: {lead.company}")
        print(f"  Sector: {lead.sector}")
        print(f"  Source: {lead.source}")
        print(f"  Created: {lead.created_at}")
        
        return lead


async def main():
    """Run all tests."""
    print("=== Marketing Funnel End-to-End Test ===\n")
    
    # Step 1: Create tables
    print("Step 1: Creating database tables...")
    await create_tables()
    print()
    
    # Step 2: Test lead creation
    print("Step 2: Testing lead creation...")
    lead = await test_lead_creation()
    print()
    
    print("=== All Tests Passed ✓ ===")
    print("\nNext steps:")
    print("1. Start the server: uvicorn app.main:app --reload")
    print("2. Visit: http://localhost:8000/")
    print("3. Fill the form and submit")
    print("4. Check API docs: http://localhost:8000/api/v1/docs")


if __name__ == "__main__":
    asyncio.run(main())
