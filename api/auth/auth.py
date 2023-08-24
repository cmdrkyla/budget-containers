import os
import uuid
from flask import abort, jsonify, request, session
from datetime import timedelta

from auth.password import Password
from config import SESSION_TIMEOUT_MINUTES
from functions import datetime_now, datetime_utcnow
from models.user import User


class Auth():
    def __init__(self):
        pass

    # Login form endpoint
    @classmethod
    def login(self):
        try:
            email_address = request.form.get("email_address")
            password = request.form.get("password")
            remember_me = request.form.get("remember_me", False, bool)
        except AttributeError:
            abort(400)
        # Try to authenticate
        user = Auth.authenticate(email_address, password)
        if user:
            # Store token for after session expires
            if remember_me:
                cookie_token = self.generate_token()
                user.cookie_token = cookie_token
                user.update(user.id)
            else:
                cookie_token = None

            return jsonify({
                "success": True,
                "cookie_token": cookie_token,
            })
        else:
            abort(401)

    @classmethod
    def logout(self):
        # Update time to now (expired) to be safe
        session["valid_until"] = datetime_utcnow()
        session["cookie_token"] = ""
        session.clear()
        return jsonify({"success": True})


    # Authenticate user against database
    @classmethod
    def authenticate(self, email_address: str, password: str):
        # Find user by email
        found_user = DB().storage().select_record_by_field(
            "user", "email_address", email_address
        )
        
        # Validate the password
        if Password.check_password(password, found_user["password_hash"]):
            # Create the session
            session["user_id"] = found_user["id"]
            session["email_address"] = found_user["email_address"]
            session["valid_until"] = self.valid_until()
            return User.load_model(found_user)
        else:
            return False


    # Check if user is logged in
    @classmethod
    def is_authenticated(self):
        if "email_address" in session and "valid_until" in session:
            # Can't compare with utcnow, so we pass the timezone from the saved date
            if session["valid_until"] > datetime_now(session["valid_until"].tzinfo):
                # Reset timeout
                session["valid_until"] = self.valid_until()
                return True
            else:
                session.pop("user_id", None)
                session.pop("email_address", None)
                session.pop("valid_until", None)
        return False


    # Default session timeout datetime
    @classmethod
    def valid_until(self):
        return datetime_utcnow() + timedelta(minutes=SESSION_TIMEOUT_MINUTES)
    

    # Generate token for storing as a cookie
    @classmethod
    def generate_token(self):
        # We don't need anything fancy here, just unique and long
        return str(uuid.uuid4()) + "-" + os.urandom(64).hex()