from sqlalchemy.sql import func

from database.database import db, MetadataMixin

class Activity(MetadataMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    activity_date = db.Column(db.DateTime(timezone=True), nullable=False)
    amount = db.Column(db.types.DECIMAL(8,2), nullable=False)
    container_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(50), server_default="")
    period_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False, index=True)