from app import app
from database.database import db
from models.activity import Activity
from models.container import Container
from models.period import Period
from models.user import User

def create_database() -> any:
    with app.app_context():
            db.drop_all()
            db.create_all()
            create_default_user()
            return app
    

def create_default_user() -> User:
      user = User()
      user.email_address = "eadiek@gmail.com"
      user.name_first = "Kyla"
      user.name_last = "Eadie"
      # password = 12345
      user.password_hash = "$pbkdf2-sha256$50000$1ZrT.r.XEoKw1npPSQkhRA$B/j6Xq8NQyDGmMo9WQ1mgYlwTYULKWgfm7W/ATscCGk"
      db.session.add(user)
      db.session.commit()
      return user