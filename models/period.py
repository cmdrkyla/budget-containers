from database.database import db, MetadataMixin

class Period(MetadataMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    start_date = db.Column(db.Date, nullable=False)
    stop_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, nullable=False, index=True)