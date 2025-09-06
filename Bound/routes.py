from flask import render_template
from app import app, db
from models import Case

@app.route('/')
def dashboard():
    case = Case.query.first()
    if not case:
        case = Case(case_title="My Family Law Case")
        db.session.add(case)
        db.session.commit()
    return render_template('dashboard.html', case=case)