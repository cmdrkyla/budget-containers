from flask import Flask
import os
import pytest
import tempfile
import uuid

import app
from auth.password import Password
from database.database import db
from models.user import User

# Test database setup from:
# https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/testing-flask-applications/

@pytest.fixture(scope="session")
def db_test():
    db_fd, db_fname = tempfile.mkstemp()
    app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.app.config["TESTING"] = True
    with app.app.app_context():
        app.db.create_all()

        yield app.db

        #app.db.session.remove()
        #os.close(db_fd)
        #os.unlink(db_fname)


@pytest.fixture(scope="module")
def random_user(db_test):
    user = User(
        email_address = str(uuid.uuid4()) + "@company.test",
        name_first = os.urandom(4).hex(),
        name_last = os.urandom(4).hex(),
        password_hash = Password.hash_password("12345"),
    )
    db_test.session.add(user)
    db_test.session.commit()
    return user
    