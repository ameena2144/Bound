from flask import render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from datetime import datetime, date
import json
import os
from app import app, db
from models import Case, Child, Parent, Document, Incident, Deadline, CaseNote
from document_processor import save_uploaded_file, extract_text_from_file, get_file_type, format_file_size
from openai_service import analyze_legal_document, generate_case_summary, suggest_document_category, generate_preparation_checklist, analyze_incident_severity

def safe_date_parse(date_string):
    """Safely parse a date string, returning None if invalid or empty"""
    if not date_string or date_string.strip() == '':
        return None
    try:
        return datetime.strptime(date_string.strip(), '%Y-%m-%d').date()
    except (ValueError, TypeError):
        return None

def safe_datetime_parse(datetime_string, format_string='%Y-%m-%dT%H:%M'):
    """Safely parse a datetime string, returning None if invalid or empty"""
    if not datetime_string or datetime_string.strip() == '':
        return None
    try:
        return datetime.strptime(datetime_string.strip(), format_string)
    except (ValueError, TypeError):
        return None

@app.route('/')
def dashboard():
    """Main dashboard view"""
    # Get or create default case
    case = Case.query.first()
    if not case:
        case = Case()
        case.case_title = "My Family Law Case"
        case.case_type = "Family Law"
        db.session.add(case)
        db.session.commit()
    
    # Get recent activity
    recent_documents = Document.query.filter_by(case_id=case.id).order_by(Document.created_at.desc()).limit(5).all()
    upcoming_deadlines = Deadline.query.filter_by(case_id=case.id, is_completed=False).order_by(Deadline.deadline_date).limit(5).all()
    recent_incidents = Incident.query.filter_by(case_id=case.id).order_by(Incident.created_at.desc()).limit(3).all()
    
    # Calculate statistics
    stats = {
        'total_children': Child.query.filter_by(case_id=case.id).count(),
        'total_parents': Parent.query.filter_by(case_id=case.id).count(),
        'total_documents': Document.query.filter_by(case_id=case.id).count(),
        'open_deadlines': Deadline.query.filter_by(case_id=case.id, is_completed=False).count(),
        'total_incidents': Incident.query.filter_by(case_id=case.id).count()
    }
    
    return render_template('dashboard.html', case=case, stats=stats, 
                         recent_documents=recent_documents, upcoming_deadlines=upcoming_deadlines,
                         recent_incidents=recent_incidents)

@app.route('/children')
def children_profiles():
    """Children profiles management"""
    case = Case.query.first()
    if not case:
        return redirect(url_for('dashboard'))
    
    children = Child.query.filter_by(case_id=case.id).all()
    return render_template('children_profiles.html', case=case, children=children)

@app.route('/children/add', methods=['GET', 'POST'])
def add_child():
    """Add new child profile"""
    case = Case.query.first()
    if not case:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        child = Child()
        child.case_id = case.id
        child.first_name = request.form.get('first_name')
        child.last_name = request.form.get('last_name')
        child.date_of_birth = safe_date_parse(request.form.get('date_of_birth'))
        child.gender = request.form.get('gender')
        child.school_name = request.form.get('school_name')
        child.grade_level = request.form.get('grade_level')
        child.school_address = request.form.get('school_address')
        child.school_phone = request.form.get('school_phone')
        child.primary_doctor = request.form.get('primary_doctor')
        child.medical_conditions = request.form.get('medical_conditions')
        child.medications = request.form.get('medications')
        child.allergies = request.form.get('allergies')
        child.insurance_info = request.form.get('insurance_info')
        child.activities = request.form.get('activities')
        child.preferences = request.form.get('preferences')
        child.special_needs = request.form.get('special_needs')
        child.current_residence = request.form.get('current_residence')
        child.residence_address = request.form.get('residence_address')
        
        db.session.add(child)
        db.session.commit()
        flash('Child profile added successfully!', 'success')
        return redirect(url_for('children_profiles'))
    
    return render_template('forms/child_form.html', case=case, child=None)

@app.route('/children/<int:child_id>/edit', methods=['GET', 'POST'])
def edit_child(child_id):
    """Edit child profile"""
    child = Child.query.get_or_404(child_id)
    
    if request.method == 'POST':
        child.first_name = request.form.get('first_name')
        child.last_name = request.form.get('last_name')
        child.date_of_birth = safe_date_parse(request.form.get('date_of_birth'))
        child.gender = request.form.get('gender')
        child.school_name = request.form.get('school_name')
        child.grade_level = request.form.get('grade_level')
        child.school_address = request.form.get('school_address')
        child.school_phone = request.form.get('school_phone')
        child.primary_doctor = request.form.get('primary_doctor')
        child.medical_conditions = request.form.get('medical_conditions')
        child.medications = request.form.get('medications')
        child.allergies = request.form.get('allergies')
        child.insurance_info = request.form.get('insurance_info')
        child.activities = request.form.get('activities')
        child.preferences = request.form.get('preferences')
        child.special_needs = request.form.get('special_needs')
        child.current_residence = request.form.get('current_residence')
        child.residence_address = request.form.get('residence_address')
        child.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Child profile updated successfully!', 'success')
        return redirect(url_for('children_profiles'))
    
    return render_template('forms/child_form.html', case=child.case, child=child)

@app.route('/parents')
def parent_profiles():
    """Parent profiles management"""
    case = Case.query.first()
    if not case:
        return redirect(url_for('dashboard'))
    
    parents = Parent.query.filter_by(case_id=case.id).all()
    return render_template('parent_profiles.html', case=case, parents=parents)

@app.route('/parents/add', methods=['GET', 'POST'])
def add_parent():
    """Add new parent profile"""
    case = Case.query.first()
    if not case:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        parent = Parent()
        parent.case_id = case.id
        parent.first_name = request.form.get('first_name')
        parent.last_name = request.form.get('last_name')
        parent.relationship_to_children = request.form.get('relationship_to_children')
        parent.date_of_birth = safe_date_parse(request.form.get('date_of_birth'))
        parent.phone = request.form.get('phone')
        parent.email = request.form.get('email')
        parent.address = request.form.get('address')
        parent.employer = request.form.get('employer')
        parent.job_title = request.form.get('job_title')
        parent.work_phone = request.form.get('work_phone')
        parent.work_address = request.form.get('work_address')
        parent.income = request.form.get('income')
        parent.housing_type = request.form.get('housing_type')
        parent.housing_stability = request.form.get('housing_stability')
        parent.criminal_history = request.form.get('criminal_history')
        parent.substance_abuse_history = request.form.get('substance_abuse_history')
        parent.mental_health_history = request.form.get('mental_health_history')
        parent.parenting_time = request.form.get('parenting_time')
        parent.parenting_concerns = request.form.get('parenting_concerns')
        
        db.session.add(parent)
        db.session.commit()
        flash('Parent profile added successfully!', 'success')
        return redirect(url_for('parent_profiles'))
    
    return render_template('forms/parent_form.html', case=case, parent=None)

@app.route('/parents/<int:parent_id>/edit', methods=['GET', 'POST'])
def edit_parent(parent_id):
    """Edit parent profile"""
    parent = Parent.query.get_or_404(parent_id)
    
    if request.method == 'POST':
        parent.first_name = request.form.get('first_name')
        parent.last_name = request.form.get('last_name')
        parent.relationship_to_children = request.form.get('relationship_to_children')
        parent.date_of_birth = safe_date_parse(request.form.get('date_of_birth'))
        parent.phone = request.form.get('phone')
        parent.email = request.form.get('email')
        parent.address = request.form.get('address')
        parent.employer = request.form.get('employer')
        parent.job_title = request.form.get('job_title')
        parent.work_phone = request.form.get('work_phone')
        parent.work_address = request.form.get('work_address')
        parent.income = request.form.get('income')
        parent.housing_type = request.form.get('housing_type')
        parent.housing_stability = request.form.get('housing_stability')
        parent.criminal_history = request.form.get('criminal_history')
        parent.substance_abuse_history = request.form.get('substance_abuse_history')
        parent.mental_health_history = request.form.get('mental_health_history')
        parent.parenting_time = request.form.get('parenting_time')
        parent.parenting_concerns = request.form.get('parenting_concerns')
        parent.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Parent profile updated successfully!', 'success')
        return redirect(url_for('parent_profiles'))
    
    return render_template('forms/parent_form.html', case=parent.case, parent=parent)

@app.route('/documents')
def documents():
    """Document management"""
    case = Case.query.first()
    if not case:
        return redirect(url_for('dashboard'))
    
    category_filter = request.args.get('category', 'all')
    
    query = Document.query.filter_by(case_id=case.id)
    if category_filter != 'all':
        query = query.filter_by(category=category_filter)
    
    documents = query.order_by(Document.created_at.desc()).all()
    
    # Get document categories for filter
    categories = db.session.query(Document.category).filter_by(case_id=case.id).distinct().all()
    categories = [cat[0] for cat in categories if cat[0]]
    
    return render_template('documents.html', case=case, documents=documents, 
                         categories=categories, current_category=category_filter, format_file_size=format_file_size)

@app.route('/documents/upload', methods=['POST'])
def upload_document():
    """Upload and process new document"""
    case = Case.query.first()
    if not case:
        return redirect(url_for('dashboard'))
    
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('documents'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('documents'))
    
    # Save the file
    result = save_uploaded_file(file, app.config['UPLOAD_FOLDER'])
    
    if not result['success']:
        flash(result['error'], 'error')
        return redirect(url_for('documents'))
    
    # Create document record
    document = Document()
    document.case_id = case.id
    document.filename = result['filename']
    document.original_filename = result['original_filename']
    document.file_path = result['file_path']
    document.file_size = result['file_size']
    document.file_type = get_file_type(result['filename'])
    document.description = request.form.get('description', '')
    document.document_date = safe_date_parse(request.form.get('document_date'))
    document.is_court_filing = bool(request.form.get('is_court_filing'))
    document.is_confidential = bool(request.form.get('is_confidential'))
    
    # Extract text and analyze with AI if it's a text-based document
    if document.file_type in ['pdf', 'doc', 'docx', 'txt']:
        try:
            text_content = extract_text_from_file(result['file_path'], document.file_type)
            if text_content and not text_content.startswith('Error'):
                # AI analysis
                analysis = analyze_legal_document(text_content, document.file_type)
                
                if 'error' not in analysis:
                    document.ai_summary = analysis.get('summary', '')
                    document.ai_key_points = json.dumps(analysis.get('key_points', []))
                    document.ai_category_suggestion = analysis.get('suggested_category', 'other')
                    document.category = document.ai_category_suggestion
                else:
                    # Fallback category suggestion
                    document.category = suggest_document_category(result['original_filename'], text_content[:500])
            else:
                document.category = suggest_document_category(result['original_filename'], '')
        except Exception as e:
            app.logger.error(f"Document analysis failed: {str(e)}")
            document.category = 'other'
    else:
        document.category = 'other'  # For images, audio files, etc.
    
    db.session.add(document)
    db.session.commit()
    
    flash('Document uploaded and analyzed successfully!', 'success')
    return redirect(url_for('documents'))

@app.route('/documents/<int:document_id>')
def view_document(document_id):
    """View document details"""
    document = Document.query.get_or_404(document_id)
    
    # Parse AI analysis
    key_points = []
    if document.ai_key_points:
        try:
            key_points = json.loads(document.ai_key_points)
        except:
            pass
    
    return render_template('document_detail.html', document=document, key_points=key_points, format_file_size=format_file_size)

@app.route('/timeline')
def timeline():
    """Case timeline view"""
    case = Case.query.first()
    if not case:
        return redirect(url_for('dashboard'))
    
    # Collect all timeline events
    events = []
    
    # Add incidents
    incidents = Incident.query.filter_by(case_id=case.id).all()
    for incident in incidents:
        events.append({
            'date': incident.incident_date,
            'type': 'incident',
            'title': incident.title,
            'description': incident.description,
            'severity': incident.severity,
            'id': incident.id
        })
    
    # Add deadlines
    deadlines = Deadline.query.filter_by(case_id=case.id).all()
    for deadline in deadlines:
        events.append({
            'date': deadline.deadline_date,
            'type': 'deadline',
            'title': deadline.title,
            'description': deadline.description,
            'priority': deadline.priority,
            'is_completed': deadline.is_completed,
            'id': deadline.id
        })
    
    # Add document dates
    documents = Document.query.filter_by(case_id=case.id).filter(Document.document_date.isnot(None)).all()
    for doc in documents:
        events.append({
            'date': datetime.combine(doc.document_date, datetime.min.time()),
            'type': 'document',
            'title': f"Document: {doc.original_filename}",
            'description': doc.description or doc.ai_summary or 'Document filed',
            'category': doc.category,
            'id': doc.id
        })
    
    # Sort events by date
    events.sort(key=lambda x: x['date'], reverse=True)
    
    return render_template('timeline.html', case=case, events=events)

@app.route('/incidents')
def incidents():
    """Incident management"""
    case = Case.query.first()
    if not case:
        return redirect(url_for('dashboard'))
    
    incidents = Incident.query.filter_by(case_id=case.id).order_by(Incident.incident_date.desc()).all()
    return render_template('incidents.html', case=case, incidents=incidents)

@app.route('/incidents/add', methods=['GET', 'POST'])
def add_incident():
    """Add new incident"""
    case = Case.query.first()
    if not case:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        incident = Incident()
        incident.case_id = case.id
        incident.incident_date = safe_datetime_parse(request.form.get('incident_date'))
        incident.incident_type = request.form.get('incident_type')
        incident.severity = request.form.get('severity')
        incident.title = request.form.get('title')
        incident.description = request.form.get('description')
        incident.location = request.form.get('location')
        incident.children_involved = request.form.get('children_involved')
        incident.other_party_involved = bool(request.form.get('other_party_involved'))
        incident.witnesses = request.form.get('witnesses')
        incident.police_report = bool(request.form.get('police_report'))
        incident.police_report_number = request.form.get('police_report_number')
        incident.photos_taken = bool(request.form.get('photos_taken'))
        incident.documentation_notes = request.form.get('documentation_notes')
        incident.action_taken = request.form.get('action_taken')
        incident.follow_up_needed = bool(request.form.get('follow_up_needed'))
        incident.follow_up_date = safe_date_parse(request.form.get('follow_up_date'))
        
        # AI analysis of incident
        try:
            analysis = analyze_incident_severity(incident.description, incident.incident_type)
            if 'error' not in analysis:
                # Update severity if AI suggests different level
                ai_severity = analysis.get('severity_assessment', incident.severity)
                if ai_severity in ['low', 'medium', 'high', 'critical']:
                    incident.severity = ai_severity
        except Exception as e:
            app.logger.error(f"Incident analysis failed: {str(e)}")
        
        db.session.add(incident)
        db.session.commit()
        flash('Incident logged successfully!', 'success')
        return redirect(url_for('incidents'))
    
    # Get children for selection
    children = Child.query.filter_by(case_id=case.id).all()
    return render_template('forms/incident_form.html', case=case, incident=None, children=children)

@app.route('/deadlines')
def deadlines():
    """Deadline management"""
    case = Case.query.first()
    if not case:
        return redirect(url_for('dashboard'))
    
    # Get upcoming and overdue deadlines
    now = datetime.now()
    upcoming = Deadline.query.filter_by(case_id=case.id, is_completed=False).filter(Deadline.deadline_date >= now).order_by(Deadline.deadline_date).all()
    overdue = Deadline.query.filter_by(case_id=case.id, is_completed=False).filter(Deadline.deadline_date < now).order_by(Deadline.deadline_date).all()
    completed = Deadline.query.filter_by(case_id=case.id, is_completed=True).order_by(Deadline.deadline_date.desc()).limit(10).all()
    
    return render_template('deadlines.html', case=case, upcoming=upcoming, overdue=overdue, completed=completed)

@app.route('/deadlines/add', methods=['POST'])
def add_deadline():
    """Add new deadline"""
    case = Case.query.first()
    if not case:
        return redirect(url_for('dashboard'))
    
    deadline = Deadline()
    deadline.case_id = case.id
    deadline.title = request.form.get('title')
    deadline.deadline_date = safe_datetime_parse(request.form.get('deadline_date'))
    deadline.deadline_type = request.form.get('deadline_type')
    deadline.description = request.form.get('description')
    deadline.location = request.form.get('location')
    deadline.priority = request.form.get('priority', 'medium')
    
    db.session.add(deadline)
    db.session.commit()
    flash('Deadline added successfully!', 'success')
    return redirect(url_for('deadlines'))

@app.route('/deadlines/<int:deadline_id>/complete', methods=['POST'])
def complete_deadline(deadline_id):
    """Mark deadline as completed"""
    deadline = Deadline.query.get_or_404(deadline_id)
    deadline.is_completed = True
    deadline.completion_notes = request.form.get('completion_notes', '')
    db.session.commit()
    flash('Deadline marked as completed!', 'success')
    return redirect(url_for('deadlines'))

@app.route('/case-notes')
def case_notes():
    """Case notes management"""
    case = Case.query.first()
    if not case:
        return redirect(url_for('dashboard'))
    
    note_type = request.args.get('type', 'all')
    
    query = CaseNote.query.filter_by(case_id=case.id)
    if note_type != 'all':
        query = query.filter_by(note_type=note_type)
    
    notes = query.order_by(CaseNote.created_at.desc()).all()
    
    return render_template('case_notes.html', case=case, notes=notes, current_type=note_type)

@app.route('/case-notes/add', methods=['POST'])
def add_case_note():
    """Add new case note"""
    case = Case.query.first()
    if not case:
        return redirect(url_for('dashboard'))
    
    note = CaseNote()
    note.case_id = case.id
    note.title = request.form.get('title')
    note.content = request.form.get('content')
    note.note_type = request.form.get('note_type', 'general')
    note.tags = request.form.get('tags')
    note.is_important = bool(request.form.get('is_important'))
    note.is_confidential = bool(request.form.get('is_confidential'))
    
    db.session.add(note)
    db.session.commit()
    flash('Case note added successfully!', 'success')
    return redirect(url_for('case_notes'))

@app.route('/case-summary')
def case_summary():
    """Generate AI-powered case summary"""
    case = Case.query.first()
    if not case:
        return redirect(url_for('dashboard'))
    
    # Collect case data
    case_data = {
        'case_info': {
            'title': case.case_title,
            'type': case.case_type,
            'court': case.court_name
        },
        'children': [
            {
                'name': f"{child.first_name} {child.last_name}",
                'age': (date.today() - child.date_of_birth).days // 365 if child.date_of_birth else None,
                'current_residence': child.current_residence,
                'school': child.school_name,
                'medical_conditions': child.medical_conditions,
                'special_needs': child.special_needs
            } for child in Child.query.filter_by(case_id=case.id).all()
        ],
        'parents': [
            {
                'name': f"{parent.first_name} {parent.last_name}",
                'relationship': parent.relationship_to_children,
                'employment': parent.employer,
                'concerns': parent.parenting_concerns
            } for parent in Parent.query.filter_by(case_id=case.id).all()
        ],
        'recent_incidents': [
            {
                'type': incident.incident_type,
                'severity': incident.severity,
                'description': incident.description[:200]
            } for incident in Incident.query.filter_by(case_id=case.id).order_by(Incident.incident_date.desc()).limit(5).all()
        ]
    }
    
    # Generate AI summary
    summary = generate_case_summary(case_data)
    
    return render_template('case_summary.html', case=case, summary=summary)

@app.route('/preparation-checklist')
def preparation_checklist():
    """Generate preparation checklist"""
    case = Case.query.first()
    if not case:
        return redirect(url_for('dashboard'))
    
    hearing_type = request.args.get('hearing_type', 'general')
    checklist = generate_preparation_checklist(case.case_type, hearing_type)
    
    return render_template('preparation_checklist.html', case=case, checklist=checklist)

# File serving route for uploaded documents
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
