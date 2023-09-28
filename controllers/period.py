from datetime import datetime
from flask import jsonify, request
from sqlalchemy.sql import func

import app
from database.database import db, row_to_dict, rows_to_list
from models.period import Period

class PeriodController():
    def create() -> dict:
        try:
            period = Period()
            period.start_date = datetime.strptime(
                request.json.get("start_date"), "%Y-%m-%d"
            )
            period.stop_date = datetime.strptime(
                request.json.get("stop_date"), "%Y-%m-%d"
            )
            period.user_id = int(request.json.get("user_id"))
            db.session.add(period)
            db.session.commit()
            return row_to_dict(period)
        except Exception as ex:
            app.app.logger.error(f"Error creating record: {str(ex)}")
            return


    def read(id) -> dict:
        try:
            period = db.session.query(Period).filter(Period.id == id).one()
            return row_to_dict(period)
        except Exception as ex:
            app.app.logger.error(f"Error reading record: {str(ex)}")
            return


    def update(id) -> dict:
        try:
            period = db.session.query(Period).filter(Period.id == id).one()
            if request.json.get("start_date"):
                period.start_date = datetime.strptime(
                    request.json.get("start_date"), "%Y-%m-%d"
                )
            if request.json.get("stop_date"):
                period.stop_date = datetime.strptime(
                    request.json.get("stop_date"), "%Y-%m-%d"
                )
            if request.json.get("user_id"):
                period.user_id = int(request.json.get("user_id"))
            db.session.add(period)
            db.session.commit()
            return row_to_dict(period)
        except Exception as ex:
            app.app.logger.error(f"Error updating record: {str(ex)}")
            return


    def delete(id) -> dict:
        try:
            period = db.session.query(Period).filter(Period.id == id).one()
            period.deactivated_at = func.now()
            db.session.add(period)
            db.session.commit()
            return row_to_dict(period)
        except Exception as ex:
            app.app.logger.error(f"Error deleting record: {str(ex)}")
            return
        

    def list() -> list[dict]:
        try:
            periods = db.session.query(Period).filter(
                Period.deactivated_at == None
            ).order_by(Period.start_date).all()
            return rows_to_list(periods)
        except Exception as ex:
            app.app.logger.error(f"Error listing records: {str(ex)}")
            return