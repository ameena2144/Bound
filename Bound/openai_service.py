import json
import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

openai = OpenAI(api_key=OPENAI_API_KEY)

def analyze_legal_document(text, document_type=None):
    """Analyze a legal document and extract key information"""
    try:
        system_prompt = """You are a legal document analysis expert specializing in family law and child custody cases. 
        Analyze the provided document and extract key information that would be relevant for a self-represented litigant.
        Focus on important dates, obligations, restrictions, rights, and any information relevant to children's best interests.
        
        Provide your analysis in JSON format with the following structure:
        {
            "summary": "Brief summary of the document",
            "key_points": ["List of important points"],
            "important_dates": ["List of dates and deadlines mentioned"],
            "obligations": ["List of obligations or requirements"],
            "restrictions": ["List of restrictions or limitations"],
            "children_related": ["Points specifically related to children"],
            "suggested_category": "Suggested document category",
            "action_items": ["Things the user should do based on this document"],
            "red_flags": ["Any concerning issues that need attention"]
        }"""
        
        user_prompt = f"""Please analyze this legal document:

Document Type: {document_type or 'Unknown'}

Document Content:
{text}"""

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        if content:
            return json.loads(content)
        else:
            raise ValueError("Empty response from OpenAI")
            
    except Exception as e:
        return {
            "error": f"Failed to analyze document: {str(e)}",
            "summary": "Document analysis failed",
            "key_points": [],
            "important_dates": [],
            "obligations": [],
            "restrictions": [],
            "children_related": [],
            "suggested_category": "other",
            "action_items": [],
            "red_flags": []
        }

def generate_case_summary(case_data):
    """Generate a comprehensive case summary focusing on children's best interests"""
    try:
        system_prompt = """You are a family law case analysis expert. Generate a comprehensive case summary 
        that focuses on the children's best interests and helps a self-represented litigant understand their case.
        
        Provide your analysis in JSON format with:
        {
            "executive_summary": "Overall case summary",
            "children_best_interests": "Analysis focused on children's wellbeing",
            "key_strengths": ["Strengths in the case"],
            "areas_of_concern": ["Areas that need attention"],
            "recommended_actions": ["Specific actions to take"],
            "documentation_gaps": ["Missing documentation that should be obtained"],
            "legal_considerations": ["Important legal points to consider"]
        }"""
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this family law case: {json.dumps(case_data)}"}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        if content:
            return json.loads(content)
        else:
            raise ValueError("Empty response from OpenAI")
            
    except Exception as e:
        return {
            "error": f"Failed to generate case summary: {str(e)}",
            "executive_summary": "Case summary generation failed",
            "children_best_interests": "Unable to analyze at this time",
            "key_strengths": [],
            "areas_of_concern": [],
            "recommended_actions": [],
            "documentation_gaps": [],
            "legal_considerations": []
        }

def suggest_document_category(filename, content_preview):
    """Suggest the most appropriate category for a document"""
    try:
        categories = [
            "court_order", "custody_agreement", "medical", "school", 
            "correspondence", "financial", "police_report", "evaluation", "other"
        ]
        
        prompt = f"""Based on the filename "{filename}" and content preview below, 
        suggest the most appropriate category from these options: {', '.join(categories)}.
        
        Content preview:
        {content_preview[:500]}
        
        Respond with just the category name."""
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )
        
        content = response.choices[0].message.content
        if content:
            suggested = content.strip().lower()
            return suggested if suggested in categories else "other"
        else:
            return "other"
    except Exception:
        return "other"

def generate_preparation_checklist(case_type, hearing_type=None):
    """Generate a case preparation checklist"""
    try:
        system_prompt = """You are a family law preparation expert. Create a detailed preparation checklist 
        for a self-represented litigant. Focus on practical, actionable items that will help them be prepared.
        
        Provide the checklist in JSON format:
        {
            "checklist_title": "Title for this checklist",
            "preparation_items": [
                {
                    "category": "Category name",
                    "items": ["List of specific action items"],
                    "priority": "high/medium/low"
                }
            ],
            "timeline_suggestions": ["When to complete items"],
            "common_mistakes": ["Common mistakes to avoid"]
        }"""
        
        user_prompt = f"""Create a preparation checklist for:
        Case Type: {case_type}
        Hearing Type: {hearing_type or 'General case preparation'}"""
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        if content:
            return json.loads(content)
        else:
            raise ValueError("Empty response from OpenAI")
            
    except Exception as e:
        return {
            "error": f"Failed to generate checklist: {str(e)}",
            "checklist_title": "Case Preparation Checklist",
            "preparation_items": [],
            "timeline_suggestions": [],
            "common_mistakes": []
        }

def analyze_incident_severity(incident_description, incident_type):
    """Analyze the severity and implications of an incident"""
    try:
        system_prompt = """You are a family law incident analysis expert. Analyze incidents in custody cases 
        to help determine severity and appropriate responses.
        
        Respond in JSON format:
        {
            "severity_assessment": "low/medium/high/critical",
            "legal_implications": "Potential legal implications",
            "recommended_actions": ["Immediate actions to take"],
            "documentation_needs": ["What should be documented"],
            "follow_up_suggestions": ["Follow-up actions needed"]
        }"""
        
        user_prompt = f"""Analyze this incident:
        Type: {incident_type}
        Description: {incident_description}"""
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        if content:
            return json.loads(content)
        else:
            raise ValueError("Empty response from OpenAI")
            
    except Exception as e:
        return {
            "error": f"Failed to analyze incident: {str(e)}",
            "severity_assessment": "medium",
            "legal_implications": "Unable to assess at this time",
            "recommended_actions": [],
            "documentation_needs": [],
            "follow_up_suggestions": []
        }