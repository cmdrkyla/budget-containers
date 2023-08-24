import enum

from database.database import db, MetadataMixin

class PeriodType(enum.Enum):
    WEEKLY = "Weekly"
    BIWEEKLY = "Bi-weekly"
    MONTHLY = "Monthly"


class Period(MetadataMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    period_type = db.Column(db.Enum(PeriodType))
    start_date = db.Column(db.Date, nullable=False)
    stop_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, nullable=False, index=True)
