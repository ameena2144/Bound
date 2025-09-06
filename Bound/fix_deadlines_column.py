from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')

def fix_deadlines_column():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Check if completed column exists and rename it to is_completed
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'deadlines' AND column_name = 'completed'
        """)
        
        if cursor.fetchone():
            cursor.execute("ALTER TABLE deadlines RENAME COLUMN completed TO is_completed")
            print("✅ Renamed 'completed' column to 'is_completed' in deadlines table")
        else:
            # If neither exists, add the is_completed column
            cursor.execute("ALTER TABLE deadlines ADD COLUMN is_completed BOOLEAN DEFAULT FALSE")
            print("✅ Added is_completed column to deadlines table")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Deadlines column fix completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_deadlines_column()
