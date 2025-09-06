#!/usr/bin/env python3
"""
Complete fix for the Flask app - one script to fix everything
"""
import os

def create_working_app():
    """Create a completely working Flask app from scratch"""
    
    # 1. Fix app.py
    app_content = '''import os
import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(16))

db = SQLAlchemy(app)

if __name__ == '__main__':
    with app.app_context():
        from models import Case, Child, Parent, Document, Incident, Deadline, CaseNote
        from routes import *
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)'''
    
    with open('app.py', 'w') as f:
        f.write(app_content)
    
    # 2. Create working models.py
    models_content = '''from datetime import datetime
from app import db

class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String(100))
    case_title = db.Column(db.String(200), nullable=False, default='My Family Law Case')
    case_type = db.Column(db.String(100), default='Family Law')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Child(db.Model):
    __tablename__ = 'children'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Parent(db.Model):
    __tablename__ = 'parents'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    filename = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Incident(db.Model):
    __tablename__ = 'incidents'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Deadline(db.Model):
    __tablename__ = 'deadlines'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    deadline_date = db.Column(db.Date, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CaseNote(db.Model):
    __tablename__ = 'case_notes'
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)'''
    
    with open('models.py', 'w') as f:
        f.write(models_content)
    
    # 3. Create basic routes.py
    routes_content = '''from flask import render_template
from app import app, db
from models import Case

@app.route('/')
def dashboard():
    case = Case.query.first()
    if not case:
        case = Case(case_title="My Family Law Case")
        db.session.add(case)
        db.session.commit()
    return render_template('dashboard.html', case=case)'''
    
    with open('routes.py', 'w') as f:
        f.write(routes_content)
    
    print("Created working Flask app")

def clear_cache():
    """Clear all Python cache"""
    os.system("find . -name '*.pyc' -delete")
    os.system("find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null")
    print("Cleared cache")

if __name__ == "__main__":
    print("Fixing your app completely...")
    clear_cache()
    create_working_app()
    print("Done! Test with: python app.py")
