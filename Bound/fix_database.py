from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')

def add_missing_column():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'cases' AND column_name = 'case_title'
        """)
        
        if cursor.fetchone() is None:
            print("Adding case_title column...")
            cursor.execute("ALTER TABLE cases ADD COLUMN case_title VARCHAR(200)")
            conn.commit()
            print("case_title column added successfully")
        else:
            print("case_title column already exists")
        
        cursor.close()
        conn.close()
        print("Database fix completed!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_missing_column()
