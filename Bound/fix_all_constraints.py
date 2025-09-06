from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')

def fix_all_constraints():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Get all NOT NULL constraints in cases table
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'cases' 
            AND is_nullable = 'NO' 
            AND column_name NOT IN ('id', 'created_at')
        """)
        
        not_null_columns = [row[0] for row in cursor.fetchall()]
        print(f"Found NOT NULL columns: {not_null_columns}")
        
        # Remove NOT NULL constraints from all columns except id and created_at
        for column in not_null_columns:
            try:
                cursor.execute(f"ALTER TABLE cases ALTER COLUMN {column} DROP NOT NULL")
                print(f"✅ Removed NOT NULL constraint from {column}")
            except Exception as e:
                print(f"⚠️  Could not modify {column}: {e}")
        
        conn.commit()
        
        # Show final table structure
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'cases'
            ORDER BY ordinal_position
        """)
        
        print("\nFinal cases table structure:")
        for row in cursor.fetchall():
            print(f"  - {row[0]} ({row[1]}) - Nullable: {row[2]}")
            
        cursor.close()
        conn.close()
        print("\n✅ All constraints fixed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_all_constraints()
