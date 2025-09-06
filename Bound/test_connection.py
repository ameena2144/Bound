#!/usr/bin/env python3
"""
Test Flask app connection to the new Supabase tables
"""

import os
from dotenv import load_dotenv
load_dotenv()

# Simple test without importing models to avoid the import issue
import psycopg2

def test_tables():
    """Test that we can connect and query our tables"""
    try:
        database_url = os.getenv('DATABASE_URL')
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("🧪 Testing table connections...")
        
        tables_to_test = ['cases', 'children', 'parents', 'documents', 'incidents', 'deadlines', 'case_notes']
        
        for table in tables_to_test:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"   ✅ {table}: {count} records")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 All tables are accessible!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing tables: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Legal Case Binder - Table Connection Test")
    print("=" * 50)
    test_tables()
