from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class MetadataMixin(object):
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    deactivated_at = db.Column(db.DateTime(timezone=True), nullable=True)
    modified_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# Turn sqlalchemy row into dict
def row_to_dict(row:object) -> dict:
    row_dict = {}
    for property in row.__table__.columns.keys():
        # Is it an enum
        if isinstance(getattr(row, property), Enum):
            row_dict[property] = getattr(row, property).value
        else:
            row_dict[property] = getattr(row, property)
    return row_dict



# Turn sqlalchemy rows into list of dicts
def rows_to_list(rows:object) -> list[dict]:
    results = []
    for row in rows:
        results.append(row_to_dict(row))
    return results