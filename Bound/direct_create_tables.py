#!/usr/bin/env python3
"""
Direct PostgreSQL table creation script
"""

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_tables_directly():
    """Create tables directly using PostgreSQL"""
    
    # Get database URL
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ No DATABASE_URL found in environment")
        return False
    
    try:
        print("🚀 Connecting to PostgreSQL database...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("📋 Creating tables...")
        
        # Create cases table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cases (
                id SERIAL PRIMARY KEY,
                case_number VARCHAR(100) UNIQUE NOT NULL,
                client_name VARCHAR(200) NOT NULL,
                case_type VARCHAR(100),
                status VARCHAR(50) DEFAULT 'Open',
                court VARCHAR(200),
                judge VARCHAR(200),
                opposing_counsel VARCHAR(200),
                case_summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create children table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS children (
                id SERIAL PRIMARY KEY,
                case_id INTEGER REFERENCES cases(id) ON DELETE CASCADE,
                name VARCHAR(200) NOT NULL,
                date_of_birth DATE,
                age INTEGER,
                gender VARCHAR(20),
                current_placement VARCHAR(200),
                school VARCHAR(200),
                medical_needs TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create parents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parents (
                id SERIAL PRIMARY KEY,
                case_id INTEGER REFERENCES cases(id) ON DELETE CASCADE,
                name VARCHAR(200) NOT NULL,
                relationship VARCHAR(100),
                address TEXT,
                phone VARCHAR(50),
                email VARCHAR(200),
                employment VARCHAR(200),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create documents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                case_id INTEGER REFERENCES cases(id) ON DELETE CASCADE,
                filename VARCHAR(300) NOT NULL,
                original_filename VARCHAR(300),
                file_type VARCHAR(100),
                file_size INTEGER,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                document_type VARCHAR(100),
                description TEXT,
                extracted_text TEXT
            );
        """)
        
        # Create incidents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id SERIAL PRIMARY KEY,
                case_id INTEGER REFERENCES cases(id) ON DELETE CASCADE,
                incident_date DATE NOT NULL,
                incident_type VARCHAR(100),
                description TEXT NOT NULL,
                location VARCHAR(200),
                reporter VARCHAR(200),
                severity VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create deadlines table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deadlines (
                id SERIAL PRIMARY KEY,
                case_id INTEGER REFERENCES cases(id) ON DELETE CASCADE,
                title VARCHAR(200) NOT NULL,
                deadline_date DATE NOT NULL,
                description TEXT,
                priority VARCHAR(20) DEFAULT 'Medium',
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create case_notes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS case_notes (
                id SERIAL PRIMARY KEY,
                case_id INTEGER REFERENCES cases(id) ON DELETE CASCADE,
                note_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                note_type VARCHAR(100),
                content TEXT NOT NULL,
                author VARCHAR(200),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Commit the changes
        conn.commit()
        
        # Check what tables were created
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"\n✅ Successfully created {len(tables)} tables:")
        for table in tables:
            print(f"   • {table[0]}")
            
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Legal Case Binder - Direct PostgreSQL Table Creation")
    print("=" * 60)
    
    success = create_tables_directly()
    
    if success:
        print("\n🎉 Tables created successfully!")
        print("You can now check your Supabase dashboard to see the tables.")
    else:
        print("\n💥 Table creation failed. Check the error message above.")
