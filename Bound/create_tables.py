#!/usr/bin/env python3
"""
Database migration script to create all tables in Supabase PostgreSQL
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our app and database (models are already imported in app.py)
from app import app, db

def create_tables():
    """Create all database tables"""
    try:
        print("🚀 Starting database table creation...")
        
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ All tables created successfully!")
            
            # Let's verify what tables were created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"\n📋 Created {len(tables)} tables:")
            for table in sorted(tables):
                print(f"   • {table}")
                
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Legal Case Binder - Database Migration")
    print("=" * 50)
    
    success = create_tables()
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print("You can now check your Supabase dashboard to see the tables.")
    else:
        print("\n💥 Migration failed. Check the error message above.")
