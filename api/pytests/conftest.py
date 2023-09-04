import os
import pytest
import uuid

from app import app
from auth.password import Password
from database.database import db
from models.user import User

app.app_context().push()
db.create_all()

@pytest.fixture(scope="module")
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
    