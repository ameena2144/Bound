from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')

def fix_case_number_constraint():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Make case_number nullable
        cursor.execute("ALTER TABLE cases ALTER COLUMN case_number DROP NOT NULL")
        
        # Also check if there are other NOT NULL constraints we need to remove
        cursor.execute("ALTER TABLE cases ALTER COLUMN status DROP NOT NULL")
        
        conn.commit()
        print("✅ Fixed case_number and status constraints - they can now be NULL")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_case_number_constraint()
