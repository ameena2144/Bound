# Legal Case Binder

## Overview

Legal Case Binder is a comprehensive case management system designed specifically for self-represented litigants in family law and child custody cases. The application helps users organize legal documents, track case timelines, manage child and parent profiles, monitor deadlines, and receive AI-powered document analysis and case preparation guidance. Built with Flask and SQLAlchemy, it features an intuitive web interface with Bootstrap styling and integrates with OpenAI for intelligent document processing and legal insights.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Web Framework**: Flask-based application with SQLAlchemy ORM for database operations
- **Database Layer**: SQLite for development with PostgreSQL compatibility built-in through SQLAlchemy configuration
- **Model Structure**: Comprehensive data models for Cases, Children, Parents, Documents, Incidents, Deadlines, and Case Notes with proper relationships and cascading deletes
- **File Processing**: Custom document processor supporting multiple file types (PDF, DOCX, images, audio) with text extraction capabilities
- **Session Management**: Flask sessions with configurable secret keys and proxy handling for deployment

### Frontend Architecture  
- **Template Engine**: Jinja2 templates with a base template system for consistent layout
- **UI Framework**: Bootstrap with dark theme styling and Feather Icons for consistent iconography
- **Client-side Features**: JavaScript enhancements for form validation, file uploads, timeline filtering, and auto-save functionality
- **Responsive Design**: Mobile-first approach with Bootstrap grid system and custom CSS for legal-specific styling

### AI Integration
- **Document Analysis**: OpenAI GPT-4o integration for intelligent document processing, categorization, and key information extraction
- **Case Preparation**: AI-generated preparation checklists for different hearing types (court hearings, mediation, custody evaluation)
- **Legal Insights**: Automated case summaries focusing on children's best interests and legal strategy recommendations
- **Incident Analysis**: AI-powered severity assessment and follow-up recommendations for incident logging

### Data Management
- **File Storage**: Local file system with configurable upload directory and 16MB file size limits
- **Document Processing**: Text extraction from PDF and DOCX files with secure filename handling using UUIDs
- **Timeline Management**: Chronological event tracking combining documents, incidents, and deadlines in unified timeline views
- **Search and Filtering**: Category-based filtering for documents, incidents, and case notes with real-time client-side filtering

## External Dependencies

### Core Dependencies
- **Flask**: Web framework with SQLAlchemy extension for database operations
- **OpenAI API**: GPT-4o model for document analysis, case summaries, and preparation guidance
- **PyPDF2**: PDF text extraction and processing
- **python-docx**: Microsoft Word document processing and text extraction
- **Werkzeug**: File upload handling with security utilities

### Frontend Dependencies
- **Bootstrap 5**: UI framework with dark theme from Replit CDN
- **Feather Icons**: Icon library for consistent interface elements
- **Custom CSS**: Legal-specific styling extensions for timeline views and form layouts

### Database Configuration
- **Development**: SQLite with local file storage
- **Production Ready**: PostgreSQL compatibility through SQLAlchemy DATABASE_URL configuration
- **Connection Pooling**: Configured with pool recycling and pre-ping for production reliability