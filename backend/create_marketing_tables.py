"""Create marketing automation tables."""

from sqlalchemy import create_engine, text

# Use SQLite for local development
engine = create_engine('sqlite:///datapurity.db')

with engine.begin() as conn:
    # Create scheduled_tasks table
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS scheduled_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER NOT NULL,
            task_type VARCHAR(50) NOT NULL,
            payload TEXT NOT NULL,
            run_at TIMESTAMP NOT NULL,
            status VARCHAR(20) DEFAULT 'pending' NOT NULL,
            error_message VARCHAR(500),
            retry_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        )
    """))
    
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_scheduled_tasks_lead_id ON scheduled_tasks(lead_id)
    """))
    
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_scheduled_tasks_run_at ON scheduled_tasks(run_at)
    """))
    
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_scheduled_tasks_status ON scheduled_tasks(status)
    """))
    
    # Create campaign_events table
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS campaign_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER NOT NULL,
            event_type VARCHAR(100) NOT NULL,
            meta TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        )
    """))
    
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_campaign_events_lead_id ON campaign_events(lead_id)
    """))
    
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_campaign_events_event_type ON campaign_events(event_type)
    """))
    
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_campaign_events_created_at ON campaign_events(created_at)
    """))
    
    # Update leads table to add status column if not exists (for existing databases)
    try:
        conn.execute(text("""
            ALTER TABLE leads ADD COLUMN status VARCHAR(50) DEFAULT 'new'
        """))
    except:
        pass  # Column already exists

print('✓ Marketing automation tables created successfully!')
print('  - scheduled_tasks')
print('  - campaign_events')
print('  - leads (updated with status column)')
