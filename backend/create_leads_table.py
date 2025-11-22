"""Create leads table on server"""
from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///datapurity.db')

with engine.begin() as conn:
    # Create leads table
    conn.execute(text("""
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
    
    # Create index
    conn.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email)
    """))
    
print('✓ Leads table created successfully')
