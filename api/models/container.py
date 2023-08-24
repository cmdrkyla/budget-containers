from database.database import db, MetadataMixin

class Container(MetadataMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, nullable=False, index=True)