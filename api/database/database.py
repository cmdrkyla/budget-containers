from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class MetadataMixin(object):
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    deactivated_at = db.Column(db.DateTime(timezone=True), nullable=True)
    modified_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# Turn sqlalchemy row into dict
def row_to_dict(row):
    row.__dict__.pop('_sa_instance_state', None)
    return row.__dict__


# Turn sqlalchemy rows into list of dicts
def rows_to_list(rows):
    results = []
    for row in rows:
        results.append(row_to_dict(row))
    return results