import os
from app import app, db

if __name__ == "__main__":
    # Handle database initialization more safely
    try:
        with app.app_context():
            db.create_all()
            print("Database tables created/verified")
    except Exception as e:
        print(f"Database setup error: {e}")
        # Continue anyway - tables might already exist
    
    # Get port from environment (Render requirement)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=False)
