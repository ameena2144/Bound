#!/usr/bin/env python3
"""
Sync database schema with current Flask models
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def update_database_schema():
    """Update existing database tables to match Flask models"""
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    try:
        print("Updating database schema...")
        
        # Check if case_title column exists, if not add it
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'cases' AND column_name = 'case_title';
        """)
        
        if not cursor.fetchone():
            print("Adding case_title column...")
            cursor.execute("ALTER TABLE cases ADD COLUMN case_title VARCHAR(200) DEFAULT 'My Family Law Case';")
        
        # Update any existing records without case_title
        cursor.execute("UPDATE cases SET case_title = 'My Family Law Case' WHERE case_title IS NULL;")
        
        # Commit changes
        conn.commit()
        print("✅ Database schema updated successfully")
        
    except Exception as e:
        print(f"❌ Error updating schema: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    update_database_schema()
