from flask import jsonify, request
from sqlalchemy.sql import func

import app
from database.database import db, row_to_dict, rows_to_list
from auth.password import Password
from models.user import User

class UserController():
    def create() -> dict:
        try:
            user = User()
            user.email_address = request.form.get("email_address")
            user.name_first = request.form.get("name_first")
            user.name_last = request.form.get("name_last")
            user.password_hash = Password.hash_password(request.form.get("password"))
            db.session.add(user)
            db.session.commit()
            return row_to_dict(user)
        except Exception as ex:
            app.app.logger.error(f"Error creating record: {str(ex)}")
            return


    def read(id) -> dict:
        try:
            user = db.session.query(User).filter(User.id == id).one()
            return row_to_dict(user)
        except Exception as ex:
            app.app.logger.error(f"Error reading record: {str(ex)}")
            return


    def update(id) -> dict:
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
        except Exception as ex:
            app.app.logger.error(f"Error updating record: {str(ex)}")
            return


    def delete(id) -> dict:
        try:
            user = db.session.query(User).filter(User.id == id).one()
            user.deactivated_at = func.now()
            db.session.add(user)
            db.session.commit()
            return row_to_dict(user)
        except Exception as ex:
            app.app.logger.error(f"Error deleting record: {str(ex)}")
            return
        

    def list() -> list[dict]:
        try:
            users = db.session.query(User).filter(User.deactivated_at == None).order_by(User.email_address).all()
            return rows_to_list(users)
        except Exception as ex:
            app.app.logger.error(f"Error listing records: {str(ex)}")
            return