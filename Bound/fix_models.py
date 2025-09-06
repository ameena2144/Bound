#!/usr/bin/env python3
"""
Script to automatically add __tablename__ attributes to models
"""

def fix_models():
    # Read the current models.py file
    with open('models.py', 'r') as f:
        content = f.read()
    
    # Define the replacements needed
    replacements = [
        ('class Case(db.Model):', 'class Case(db.Model):\n    __tablename__ = \'cases\''),
        ('class Child(db.Model):', 'class Child(db.Model):\n    __tablename__ = \'children\''),
        ('class Parent(db.Model):', 'class Parent(db.Model):\n    __tablename__ = \'parents\''),
        ('class Document(db.Model):', 'class Document(db.Model):\n    __tablename__ = \'documents\''),
        ('class Incident(db.Model):', 'class Incident(db.Model):\n    __tablename__ = \'incidents\''),
        ('class Deadline(db.Model):', 'class Deadline(db.Model):\n    __tablename__ = \'deadlines\''),
        ('class CaseNote(db.Model):', 'class CaseNote(db.Model):\n    __tablename__ = \'case_notes\'')
    ]
    
    # Apply each replacement
    for old, new in replacements:
        content = content.replace(old, new)
    
    # Write the fixed content back
    with open('models.py', 'w') as f:
        f.write(content)
    
    print("Fixed models.py with __tablename__ attributes")

if __name__ == "__main__":
    fix_models()
