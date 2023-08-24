from app import app
from database.database import db
from models.activity import Activity
from models.container import Container
from models.period import Period
from models.user import User

def create_database():
    with app.app_context():
            db.drop_all()
            db.create_all()
            create_default_user()
            return app
    

def create_default_user():
      user = User()
      user.email_address = "eadiek@gmail.com"
      user.name_first = "Kyla"
      user.name_last = "Eadie"
      user.password_hash = "pbkdf2$sha256$150000$t2SfbLfZpq$b6096e2bb880bf507ea815a88271f08ba791321d1bdf4e72e3633437d60af3eb"
      db.session.add(user)
      db.session.commit()
      return user