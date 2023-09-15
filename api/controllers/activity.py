from datetime import datetime
from flask import jsonify, request
from sqlalchemy.sql import func

import app
from database.database import db, row_to_dict, rows_to_list
from models.activity import Activity

class ActivityController():
    def create() -> dict:
        try:
            activity = Activity()
            activity.activity_date = datetime.strptime(
                request.form.get("activity_date"), "%Y-%m-%d"
            )
            activity.amount = request.form.get("amount")
            activity.container_id = request.form.get("container_id")
            activity.description = request.form.get("description", "")
            activity.period_id = request.form.get("period_id")
            activity.user_id = request.form.get("user_id")
            db.session.add(activity)
            db.session.commit()
            return row_to_dict(activity)
        except Exception as ex:
            app.app.logger.error(f"Error creating record: {str(ex)}")
            return


    def read(id) -> dict:
        try:
            activity = db.session.query(Activity).filter(Activity.id == id).one()
            return row_to_dict(activity)
        except Exception as ex:
            app.app.logger.error(f"Error reading record: {str(ex)}")
            return


    def update(id) -> dict:
        try:
            activity = db.session.query(Activity).filter(Activity.id == id).one()
            activity.activity_date = request.form.get("activity_date", activity.activity_date)
            activity.amount = request.form.get("amount", activity.amount)
            activity.container_id = request.form.get("container_id", activity.container_id)
            activity.description = request.form.get("description", activity.description)
            activity.period_id = request.form.get("period_id", activity.period_id)
            activity.user_id = request.form.get("user_id", activity.user_id)
            db.session.add(activity)
            db.session.commit()
            return row_to_dict(activity)
        except Exception as ex:
            app.app.logger.error(f"Error updating record: {str(ex)}")
            return


    def delete(id) -> dict:
        try:
            activity = db.session.query(Activity).filter(Activity.id == id).one()
            activity.deactivated_at = func.now()
            db.session.add(activity)
            db.session.commit()
            return row_to_dict(activity)
        except Exception as ex:
            app.app.logger.error(f"Error deleting record: {str(ex)}")
            return
        

    def list() -> list[dict]:
        try:
            activities = db.session.query(Activity).filter(
                Activity.deactivated_at == None
            ).order_by(Activity.activity_date).all()
            return rows_to_list(activities)
        except Exception as ex:
            app.app.logger.error(f"Error listing records: {str(ex)}")
            return