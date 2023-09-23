import enum

from database.database import db, MetadataMixin

class FrequencyMonthRepeat(enum.Enum):
    SAME_DATE = "Same Date"
    SAME_WEEK = "Same Week"


class FrequencyType(enum.Enum):
    DAY = "Day"
    WEEK = "Week"
    MONTH = "Month"


class FrequencyWeekRepeat(enum.Enum):
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6


class Container(MetadataMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.types.DECIMAL(8,2), nullable=False)
    frequency_interval = db.Column(db.SmallInteger, nullable=False)
    frequency_month_repeat = db.Column(db.Enum(FrequencyMonthRepeat), nullable=True)
    frequency_type = db.Column(db.Enum(FrequencyType), nullable=False)
    frequency_week_repeat = db.Column(db.Enum(FrequencyWeekRepeat), nullable=True)
    name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, nullable=False, index=True)