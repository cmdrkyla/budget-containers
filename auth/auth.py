import os
import uuid
from flask import abort, request, session
from datetime import datetime, timedelta
import pytz

import app
from auth.password import Password
from imports.config import SESSION_TIMEOUT_MINUTES
from database.database import db
from imports.functions import datetime_now, datetime_utcnow
from models.user import User


class Auth():
    def __init__(self):
        pass

    # Login form endpoint
    @classmethod
    def login(self):
        try:
            email_address = request.json["email_address"]
            password = request.json["password"]
            if "remember_me" in request.json and request.json["remember_me"]:
                remember_me = True
            else:
                remember_me = False
        except AttributeError:
            abort(400)
        # Try to authenticate
        user = Auth.authenticate(email_address, password)
        
        if user:
            # Generate a token for the session (and possible to save)
            login_token = self.generate_token()
            # Store token for after session expires
            if remember_me:
                user.login_token = login_token
                db.session.add(user)
                db.session.commit()

            return {
                "success": True,
                "token": login_token,
            }
        else:
            abort(401)

    # Logout form endpoint
    @classmethod
    def logout(self):
        session["auth"] = None
        session.clear()
        if "auth" not in session:
            return {"success": True}
        else:
            abort(500)


    # Authenticate user against database
    @classmethod
    def authenticate(self, email_address: str, password: str):
        # Find user by email
        try:
            found_user = db.session.query(User).filter(
                User.email_address == email_address,
                User.deactivated_at == None,
            ).one()
        except:
            return False
        
        # Validate the password
        if Password.verify_password(password, found_user.password_hash):
            # Create the session
            self.create_session(found_user)
            return found_user
        else:
            return False
        
    
    # Create session variables
    @classmethod
    def create_session(self, found_user):
        session["auth"] = {}
        session["auth"]["user_id"] = found_user.id
        session["auth"]["email_address"] = found_user.email_address
        session["auth"]["valid_until"] = self.valid_until()


    # Check if user is logged in
    @classmethod
    def is_authenticated(self) -> bool:
        # Standard session
        if "auth" in session and "email_address" in session["auth"] and "valid_until" in session["auth"]:
            # Can't compare with utcnow, so we pass the timezone from the saved date
            if session["auth"]["valid_until"] > datetime_now(session["auth"]["valid_until"].tzinfo):
                # Reset timeout
                session["auth"]["valid_until"] = self.valid_until()
                return True
            else:
                # Logout
                self.logout()
                return False
        # Login token
        elif request.headers.get("X-Login-Token", None) != None:
            return self.authenticate_login_token(request.headers.get("X-Login-Token"))
        return False


    # Default session timeout datetime
    @classmethod
    def valid_until(self) -> datetime:
        return datetime_utcnow() + timedelta(minutes=SESSION_TIMEOUT_MINUTES)
    

    # Generate token for storing in local storage
    @classmethod
    def generate_token(self) -> str:
        # We don't need anything fancy here, just unique and long
        return str(uuid.uuid4()) + "-" + os.urandom(64).hex()
    
    
    @classmethod
    def authenticate_login_token(self, login_token):
        try:
            found_user = db.session.query(User).filter(
                User.login_token == login_token,
                User.deactivated_at == None,
            ).one()
            # Create the session
            self.create_session(found_user)
            return True
        except:
            return False