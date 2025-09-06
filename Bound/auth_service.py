#!/usr/bin/env python3
"""
Supabase Authentication Service
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import Optional, Dict, Any

# Load environment variables first
load_dotenv()

class AuthService:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            print(f"Debug - URL: {url}")
            print(f"Debug - Key: {key[:20]}..." if key else "None")
            raise ValueError("Missing Supabase URL or API key")
            
        self.supabase: Client = create_client(url, key)
    
    def sign_up(self, email: str, password: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Sign up a new user"""
        try:
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {"data": metadata} if metadata else {}
            })
            return {
                "success": True,
                "user": response.user,
                "session": response.session,
                "message": "Account created successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create account"
            }
    
    def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """Sign in an existing user"""
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return {
                "success": True,
                "user": response.user,
                "session": response.session,
                "message": "Signed in successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Invalid email or password"
            }
    
    def sign_out(self) -> Dict[str, Any]:
        """Sign out the current user"""
        try:
            self.supabase.auth.sign_out()
            return {
                "success": True,
                "message": "Signed out successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to sign out"
            }
    
    def get_user(self) -> Optional[Dict[str, Any]]:
        """Get current user"""
        try:
            user = self.supabase.auth.get_user()
            return user.user if user else None
        except:
            return None
    
    def reset_password(self, email: str) -> Dict[str, Any]:
        """Send password reset email"""
        try:
            self.supabase.auth.reset_password_email(email)
            return {
                "success": True,
                "message": "Password reset email sent"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to send reset email"
            }
    
    def verify_session(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Verify a session token"""
        try:
            response = self.supabase.auth.get_user(access_token)
            return response.user if response else None
        except:
            return None

# Create the auth service instance only when this module is imported
def get_auth_service():
    """Get auth service instance"""
    return AuthService()

# Only create the instance when imported, not when running standalone
if __name__ != "__main__":
    auth_service = get_auth_service()

from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
