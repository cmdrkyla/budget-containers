import datetime
import os
import pytest
import uuid

from app import app
from auth.password import Password
from database.database import db
from models.activity import Activity
from models.container import Container, FrequencyMonthRepeat, FrequencyType
from models.period import Period
from models.user import User

app.logger.info("Pytests running")
app.app_context().push()

@pytest.fixture(scope="function", autouse=True)
def test_db():
    db.create_all()
    app.logger.debug("Databases created")
    yield
    db.session.close()
    db.drop_all()
    app.logger.debug("Databases dropped")


@pytest.fixture(scope="function")
def token_user():
    user = User(
        email_address = "token@company.test",
        login_token = "testing",
        name_first = "Token",
        name_last = "User",
        password_hash = Password.hash_password("token"),
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope="function")
def random_user():
    user = User(
        email_address = str(uuid.uuid4()) + "@company.test",
        name_first = os.urandom(4).hex(),
        name_last = os.urandom(4).hex(),
        password_hash = Password.hash_password("12345"),
    )
    db.session.add(user)
    db.session.commit()
    return user


def container_monthly(user_id: int):
    container = Container(
        amount = 500,
        frequency_interval = 1,
        frequency_month_repeat = FrequencyMonthRepeat.SAME_DATE,
        frequency_type = FrequencyType.MONTH,
        name = "Allowance",
        start_date = datetime.date(2023,9,1),
        user_id = user_id,
    )
    db.session.add(container)
    db.session.commit()
    return container

def period_month(user_id: int):
    period = Period(
        start_date = datetime.date(2023,9,1),
        stop_date = datetime.date(2023,9,30),
        user_id = user_id,
    )
    db.session.add(period)
    db.session.commit()
    return period


def activity_shopping(container_id: int, period_id: int, user_id: int):
    activity = Activity(
        activity_date = datetime.date(2023,9,15),
        amount = 10.01,
        container_id = container_id,
        description = "Uptown cheapskate",
        period_id = period_id,
        user_id = user_id,
    )
    db.session.add(activity)
    db.session.commit()
    return activity


@pytest.fixture(scope="function")
def user_with_records(random_user):
    return {
        "user": random_user,
        "container": container_monthly(random_user.id),
        "period": period_month(random_user.id),
    }


@pytest.fixture(scope="function")
def user_with_activity(user_with_records):
    user_with_records["activity"] = activity_shopping(
        user_with_records["container"].id,
        user_with_records["period"].id,
        user_with_records["user"].id,
    )
    return user_with_records

