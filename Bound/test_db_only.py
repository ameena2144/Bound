#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

print("Database connection test:")
try:
    with app.app_context():
        db.engine.connect()
        print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
