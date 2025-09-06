from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')

def add_missing_columns():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Add created_at column to documents table
        try:
            cursor.execute("ALTER TABLE documents ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            print("✅ Added created_at column to documents table")
        except Exception as e:
            print(f"⚠️  created_at column might already exist: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Missing columns fix completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_missing_columns()
