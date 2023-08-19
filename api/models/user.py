from sqlalchemy.sql import func

from database.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    deactivated_at = db.Column(db.DateTime(timezone=True), nullable=True)
    modified_at = db.Column(db.DateTime(timezone=True), server_default=func.now())    
    cookie_token = db.Column(db.String(64), nullable=True)
    email_address = db.Column(db.String(100), nullable=False)
    name_first = db.Column(db.String(50), nullable=False)
    name_last = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(96), nullable=False)

"""
class User(DefaultModel):
    def __init__(
        self,
        id: int=None,
        cookie_token: str="",
        email_address: str="",
        name_first: str="",
        name_last: str="",
        password_hash: str="",
    ):
        super().__init__()
        self._id = id
        self._cookie_token = cookie_token
        self._email_address = email_address
        self._name_first = name_first
        self._name_last = name_last
        self._password_hash = password_hash

    __table_name__ = "user"

    # id
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value: int):
        self._id = value

    # cookie_token
    @property
    def cookie_token(self):
        return self._cookie_token
    @cookie_token.setter
    def cookie_token(self, value: str):
        self._cookie_token = value

    # email_address
    @property
    def email_address(self):
        return self.email_address
    @email_address.setter
    def email_address(self, value: str):
        self.email_address = value

    # name_first
    @property
    def name_first(self):
        return self._name_first
    @name_first.setter
    def name_first(self, value: str):
        self._name_first = value

    # name_last
    @property
    def name_last(self):
        return self._name_last
    @name_last.setter
    def name_last(self, value: str):
        self._name_last = value

    # password_hash
    @property
    def password_hash(self):
        return self._password_hash
    @password_hash.setter
    def password_hash(self, value: str):
        self._password_hash = value


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
"""