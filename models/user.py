from sqlalchemy.orm import deferred

from database.database import db, MetadataMixin

class User(MetadataMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email_address = db.Column(db.String(100), nullable=False, unique=True)
    login_token = deferred(db.Column(db.types.CHAR(165), nullable=True))
    name_first = db.Column(db.String(50), nullable=False)
    name_last = db.Column(db.String(50), nullable=False)
    password_hash = deferred(db.Column(db.types.CHAR(87), nullable=False))


    # Repr
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"

    # Str
    def __str__(self):
        return f"<{self.__class__.__name__} {self.email_address}>"