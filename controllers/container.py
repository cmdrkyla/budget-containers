from datetime import datetime
from flask import jsonify, request
from sqlalchemy.sql import func

import app
from database.database import db, row_to_dict, rows_to_list
from models.container import (
    Container, FrequencyMonthRepeat, FrequencyType, FrequencyWeekRepeat
)

class ContainerController():
    def create() -> dict:
        try:
            container = Container()
            container.amount = request.json.get("amount")
            container.frequency_interval = int(request.json.get("frequency_interval"))
            if request.json.get("frequency_month_repeat"):
                container.frequency_month_repeat = FrequencyMonthRepeat(
                    request.json.get("frequency_month_repeat")
                ).name
            container.frequency_type = FrequencyType(request.json.get("frequency_type")).name
            if request.json.get("frequency_week_repeat"):
                container.frequency_week_repeat = FrequencyWeekRepeat(
                    request.json.get("frequency_week_repeat")
                ).name
            container.name = request.json.get("name")
            container.start_date = datetime.strptime(
                request.json.get("start_date"), "%Y-%m-%d"
            )
            container.user_id = int(request.json.get("user_id"))
            db.session.add(container)
            db.session.commit()
            return row_to_dict(container)
        except Exception as ex:
            app.app.logger.error(f"Error creating record: {str(ex)}")
            return


    def read(id) -> dict:
        try:
            container = db.session.query(Container).filter(Container.id == id).one()
            return row_to_dict(container)
        except Exception as ex:
            app.app.logger.error(f"Error reading record: {str(ex)}")
            return


    def update(id) -> dict:
        try:
            container = db.session.query(Container).filter(Container.id == id).one()
            if request.json.get("amount"):
                container.amount = request.json.get("amount")
            if request.json.get("frequency_interval"):
                container.frequency_interval = int(request.json.get("frequency_interval"))
            if request.json.get("frequency_month_repeat"):
                container.frequency_month_repeat = FrequencyMonthRepeat(
                    request.json.get("frequency_month_repeat")
                ).name
            if request.json.get("frequency_type"):
                container.frequency_type = FrequencyType(request.json.get("frequency_type")).name
            if request.json.get("frequency_week_repeat"):
                container.frequency_week_repeat = FrequencyWeekRepeat(
                    request.json.get("frequency_week_repeat")
                ).name
            if request.json.get("name"):
                container.name = request.json.get("name")
            if request.json.get("start_date"):
                container.start_date = datetime.strptime(
                    request.json.get("start_date"), "%Y-%m-%d"
                )
            if request.json.get("user_id"):
                container.user_id = int(request.json.get("user_id"))
            db.session.add(container)
            db.session.commit()
            return row_to_dict(container)
        except Exception as ex:
            app.app.logger.error(f"Error updating record: {str(ex)}")
            return


    def delete(id) -> dict:
        try:
            container = db.session.query(Container).filter(Container.id == id).one()
            container.deactivated_at = func.now()
            db.session.add(container)
            db.session.commit()
            return row_to_dict(container)
        except Exception as ex:
            app.app.logger.error(f"Error deleting record: {str(ex)}")
            return
        

    def list() -> list[dict]:
        try:
            containers = db.session.query(Container).filter(
                Container.deactivated_at == None
            ).order_by(Container.name).all()
            return rows_to_list(containers)
        except Exception as ex:
            app.app.logger.error(f"Error listing records: {str(ex)}")
            return