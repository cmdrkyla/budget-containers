from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class MetadataMixin(object):
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    deactivated_at = db.Column(db.DateTime(timezone=True), nullable=True)
    modified_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())