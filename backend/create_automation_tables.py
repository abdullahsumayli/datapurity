"""Create tables for marketing automation."""

from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///datapurity.db')

with engine.begin() as conn:
    # Add status column to leads table
    try:
        conn.execute(text("""
            ALTER TABLE leads ADD COLUMN status VARCHAR(50) DEFAULT 'new'
        """))
        print("✓ Added status column to leads table")
    except Exception as e:
        print(f"Status column may already exist: {e}")
    
    # Create scheduled_tasks table
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS scheduled_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER NOT NULL,
            task_type VARCHAR(50) NOT NULL,
            payload JSON NOT NULL,
            run_at TIMESTAMP NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'pending',
            error_message VARCHAR(500),
            retry_count INTEGER DEFAULT 0,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        )
    """))
    
    # Create indexes for scheduled_tasks
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_scheduled_tasks_lead_id ON scheduled_tasks(lead_id)
    """))
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_scheduled_tasks_run_at ON scheduled_tasks(run_at)
    """))
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_scheduled_tasks_status ON scheduled_tasks(status)
    """))
    
    print("✓ Created scheduled_tasks table with indexes")
    
    # Create campaign_events table
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS campaign_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER NOT NULL,
            event_type VARCHAR(100) NOT NULL,
            meta JSON,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        )
    """))
    
    # Create indexes for campaign_events
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_campaign_events_lead_id ON campaign_events(lead_id)
    """))
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_campaign_events_event_type ON campaign_events(event_type)
    """))
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_campaign_events_created_at ON campaign_events(created_at)
    """))
    
    print("✓ Created campaign_events table with indexes")

print("\n✅ All tables created successfully!")
print("\nNext steps:")
print("1. Update .env with email credentials (EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_FROM)")
print("2. Start the server: uvicorn app.main:app --reload")
print("3. The scheduler will automatically start processing tasks")
