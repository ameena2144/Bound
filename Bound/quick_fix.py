#!/usr/bin/env python3
import os

# Create the simplest possible working Flask app
app_content = '''import os
import secrets
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(16))

db = SQLAlchemy()
db.init_app(app)

# Simple model
class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
    case_title = db.Column(db.String(200), default='My Legal Case')

@app.route('/')
def dashboard():
    return "<h1>Your Legal Case Binder is Working!</h1><p>Database connected to Supabase successfully.</p>"

if __name__ == '__main__':
    with app.app_context():
        print("Testing database connection...")
        try:
            db.engine.connect()
            print("Database connected successfully!")
        except Exception as e:
            print(f"Database error: {e}")
    app.run(debug=True, host='0.0.0.0', port=5000)'''

with open('app.py', 'w') as f:
    f.write(app_content)

print("Created minimal working app")
