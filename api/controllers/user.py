from flask import jsonify, request
from sqlalchemy.sql import func

from database.database import db, row_to_dict, rows_to_list
from auth.password import Password
from models.user import User

class UserController():
    def create():
        try:
            user = User()
            user.email_address = request.form.get("email_address")
            user.name_first = request.form.get("name_first")
            user.name_last = request.form.get("name_last")
            user.password_hash = Password.hash_password(request.form.get("password"))
            db.session.add(user)
            db.session.commit()
            return row_to_dict(user)
        except:
            return {}


    def read(id):
        try:
            user = db.session.query(User).filter(User.id == id).one()
            return row_to_dict(user)
        except:
            return {}


    def update(id):
        try:
            user = db.session.query(User).filter(User.id == id).one()
            user.email_address = request.form.get("email_address")
            user.name_first = request.form.get("name_first")
            user.name_last = request.form.get("name_last")
            if request.form.get("password"):
                user.password_hash = Password.hash_password(request.form.get("password"))
            db.session.add(user)
            db.session.commit()
            return row_to_dict(user)
        except:
            return {}


    def delete(id):
        try:
            user = db.session.query(User).filter(User.id == id).one()
            user.deactivated_at = func.now()
            db.session.add(user)
            db.session.commit()
            return row_to_dict(user)
        except:
            return {}
        

    def list():
        try:
            users = db.session.query(User).filter(User.deactivated_at == None).order_by(User.email_address).all()
            return rows_to_list(users)
        except:
            return []