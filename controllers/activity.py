from datetime import datetime
from decimal import Decimal
from flask import jsonify, request, session
from sqlalchemy.sql import func

import app
from database.database import db, row_to_dict, rows_to_list
from models.activity import Activity

class ActivityController():
    def create() -> dict:
        try:
            activity = Activity()
            activity.activity_date = datetime.strptime(
                request.json.get("activity_date"), "%Y-%m-%d"
            )
            activity.amount = Decimal(request.json.get("amount"))
            activity.container_id = request.json.get("container_id")
            activity.description = request.json.get("description")
            if request.json.get("period_id"):
                activity.period_id = request.json.get("period_id")
            activity.user_id = session["auth"]["user_id"]

            # Get the period if need be
            if not activity.period_id:
                # TODO: get the period from the activity_date
                activity.period_id = 1
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
            if request.form.get("activity_date"):
                activity.activity_date = datetime.strptime(
                    request.form.get("activity_date"), "%Y-%m-%d"
                )
            if request.form.get("amount"):
                activity.amount = request.form.get("amount")
            if request.form.get("container_id"):
                activity.container_id = int(request.form.get("container_id"))
            if request.form.get("description"):
                activity.description = request.form.get("description")
            if request.form.get("period_id"):
                activity.period_id = int(request.form.get("period_id"))
            if request.form.get("user_id"):
                activity.user_id = request.form.get("user_id")
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
            ).order_by(Activity.activity_date.desc()).all()
            return rows_to_list(activities)
        except Exception as ex:
            app.app.logger.error(f"Error listing records: {str(ex)}")
            return