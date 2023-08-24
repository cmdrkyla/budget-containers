from database.database import db, MetadataMixin

class User(MetadataMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)  
    cookie_token = db.Column(db.String(165), nullable=True)
    email_address = db.Column(db.String(100), nullable=False, unique=True)
    name_first = db.Column(db.String(50), nullable=False)
    name_last = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(87), nullable=False)


    # Repr
    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    # Str
    def __str__(self):
        return f"<{self.__class__.__name__} {self.id}>"

    # Json
    @classmethod
    def __to_json__(self):
        return { 
            "id": self.id,
            "email_address": self.email_address,
            "name_first": self.name_first,
            "name_last": self.name_last,
        }