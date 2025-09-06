from datetime import datetime
from app import db
from sqlalchemy.orm import relationship

class Case(db.Model):
    """Main case information"""
    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String(100))
    case_title = db.Column(db.String(200), nullable=False)
    court_name = db.Column(db.String(200))
    case_type = db.Column(db.String(100), default='Family Law')
    filing_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    children = relationship("Child", back_populates="case", cascade="all, delete-orphan")
    parents = relationship("Parent", back_populates="case", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="case", cascade="all, delete-orphan")
    incidents = relationship("Incident", back_populates="case", cascade="all, delete-orphan")
    deadlines = relationship("Deadline", back_populates="case", cascade="all, delete-orphan")
    case_notes = relationship("CaseNote", back_populates="case", cascade="all, delete-orphan")

class Child(db.Model):
    """Children information for custody cases"""
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    
    # Basic Information
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(50))
    
    # School Information
    school_name = db.Column(db.String(200))
    grade_level = db.Column(db.String(50))
    school_address = db.Column(db.Text)
    school_phone = db.Column(db.String(20))
    
    # Medical Information
    primary_doctor = db.Column(db.String(200))
    medical_conditions = db.Column(db.Text)
    medications = db.Column(db.Text)
    allergies = db.Column(db.Text)
    insurance_info = db.Column(db.Text)
    
    # Activities and Preferences
    activities = db.Column(db.Text)
    preferences = db.Column(db.Text)
    special_needs = db.Column(db.Text)
    
    # Current Living Situation
    current_residence = db.Column(db.String(20))  # 'mother', 'father', 'shared', 'other'
    residence_address = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    case = relationship("Case", back_populates="children")

class Parent(db.Model):
    """Parent/guardian information"""
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    
    # Basic Information
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    relationship_to_children = db.Column(db.String(50))  # 'mother', 'father', 'guardian'
    date_of_birth = db.Column(db.Date)
    
    # Contact Information
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    
    # Employment Information
    employer = db.Column(db.String(200))
    job_title = db.Column(db.String(100))
    work_phone = db.Column(db.String(20))
    work_address = db.Column(db.Text)
    income = db.Column(db.String(100))
    
    # Housing Information
    housing_type = db.Column(db.String(100))  # 'owned', 'rented', 'family', 'temporary'
    housing_stability = db.Column(db.Text)
    
    # Background Information
    criminal_history = db.Column(db.Text)
    substance_abuse_history = db.Column(db.Text)
    mental_health_history = db.Column(db.Text)
    
    # Parenting Information
    parenting_time = db.Column(db.Text)
    parenting_concerns = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    case = relationship("Case", back_populates="parents")

class Document(db.Model):
    """Document management"""
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    file_type = db.Column(db.String(100))
    
    # Document categorization
    category = db.Column(db.String(100))  # 'court_order', 'custody_agreement', 'medical', 'school', 'correspondence', 'financial', 'other'
    subcategory = db.Column(db.String(100))
    description = db.Column(db.Text)
    
    # AI Analysis Results
    ai_summary = db.Column(db.Text)
    ai_key_points = db.Column(db.Text)
    ai_category_suggestion = db.Column(db.String(100))
    
    # Document metadata
    document_date = db.Column(db.Date)
    is_court_filing = db.Column(db.Boolean, default=False)
    is_confidential = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    case = relationship("Case", back_populates="documents")

class Incident(db.Model):
    """Incident logging and documentation"""
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    
    incident_date = db.Column(db.DateTime, nullable=False)
    incident_type = db.Column(db.String(100))  # 'missed_visitation', 'communication_issue', 'safety_concern', 'violation', 'other'
    severity = db.Column(db.String(20))  # 'low', 'medium', 'high', 'critical'
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200))
    
    # People involved
    children_involved = db.Column(db.Text)  # JSON list of child IDs
    other_party_involved = db.Column(db.Boolean, default=False)
    witnesses = db.Column(db.Text)
    
    # Documentation
    police_report = db.Column(db.Boolean, default=False)
    police_report_number = db.Column(db.String(100))
    photos_taken = db.Column(db.Boolean, default=False)
    documentation_notes = db.Column(db.Text)
    
    # Follow-up
    action_taken = db.Column(db.Text)
    follow_up_needed = db.Column(db.Boolean, default=False)
    follow_up_date = db.Column(db.Date)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    case = relationship("Case", back_populates="incidents")

class Deadline(db.Model):
    """Important dates and deadline tracking"""
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    deadline_date = db.Column(db.DateTime, nullable=False)
    deadline_type = db.Column(db.String(100))  # 'court_hearing', 'filing_deadline', 'mediation', 'evaluation', 'other'
    
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    
    # Reminder settings
    reminder_days = db.Column(db.Integer, default=7)
    is_completed = db.Column(db.Boolean, default=False)
    completion_notes = db.Column(db.Text)
    
    # Priority
    priority = db.Column(db.String(20), default='medium')  # 'low', 'medium', 'high', 'critical'
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    case = relationship("Case", back_populates="deadlines")

class CaseNote(db.Model):
    """Case notes and journal system"""
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    note_type = db.Column(db.String(100))  # 'general', 'legal_strategy', 'communication', 'research', 'preparation'
    
    # Tagging and organization
    tags = db.Column(db.Text)  # Comma-separated tags
    is_important = db.Column(db.Boolean, default=False)
    is_confidential = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    case = relationship("Case", back_populates="case_notes")
