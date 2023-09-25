from app import app
from database.database import db
from imports.functions import date_now
from models.activity import Activity
from models.container import Container, FrequencyMonthRepeat, FrequencyType
from models.period import Period
from models.user import User

def create_database() -> any:
    with app.app_context():
            db.drop_all()
            db.create_all()
            user = create_default_user()
            container = create_default_container(user.id)
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

def create_default_container(user_id) -> Container:
      container = Container()
      container.amount = 500
      container.frequency_interval = 1
      container.frequency_month_repeat = FrequencyMonthRepeat.SAME_DATE
      container.frequency_type = FrequencyType.MONTH
      container.name = "Allowance"
      container.start_date = date_now()
      container.user_id = user_id
      db.session.add(container)
      db.session.commit()
      return container