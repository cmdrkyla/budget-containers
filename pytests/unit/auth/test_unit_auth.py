from unittest import mock
from datetime import datetime
from dateutil.relativedelta import relativedelta
from freezegun import freeze_time
import pytz

from app import app
from auth.auth import Auth, session
from auth.password import Password
from imports.config import SESSION_TIMEOUT_MINUTES
from database.database import db
from imports.functions import datetime_utcnow
from models.user import User

    
class TestAuthAuthenticate:
    @mock.patch.object(Password, "verify_password")
    def test__auth_authenticate__user_not_found(self, mock_verify_password):
        # Given - we provide a user that doesn't exist
        unknown_email_address = "unknown_email_address"
        unknown_password = "unknown_password"

        # When - we authenticate
        response = Auth.authenticate(unknown_email_address, unknown_password)

        # Then - False is returned and password is not verified
        assert response == False
        mock_verify_password.assert_not_called()


    @mock.patch.object(Password, "verify_password")
    def test__auth_authenticate__invalid_password(self, mock_verify_password, random_user):
        # Given - we provide a user and the wrong password (and mock the verification)
        invalid_password = "54321"
        mock_verify_password.return_value = False

        # When - we authenticate
        response = Auth.authenticate(random_user.email_address, invalid_password)
        # Then - False is returned and password is not verified
        assert response == False
        mock_verify_password.assert_called_once()


    @mock.patch.object(Password, "verify_password")
    @mock.patch.object(Auth, "create_session")
    def test__auth_authenticate__valid_password(
        self, mock_verify_password, mock_create_session, random_user
    ):
        # Given - we provide a user and password (and mock the verification)
        valid_password = "12345"
        mock_verify_password.return_value = True
        mock_create_session.return_value = True

        # When - we authenticate
        response = Auth.authenticate(random_user.email_address, valid_password)
        # Then - False is returned and password is not verified
        assert response == random_user
        mock_verify_password.assert_called_once()


class TestAuthCreateSession:
    def test__auth_create_session(self, random_user):
            # Given - the provided user info and context
            with app.test_request_context():
                # When - we create the session
                Auth.create_session(random_user)

                # Then - the session is created properly
                assert session["auth"]["user_id"] == random_user.id


class TestAuthIsAuthenticated:
    @mock.patch.object(Auth, "logout")
    def test__auth_is_authenticated__invalid(self, mock_logout):
        # Given - we don't setup a session
        test_is_authenticated = False
        with app.test_request_context():
            # When - we check if we are authenticated
            is_authenticated = Auth.is_authenticated()

            # Then - return false, logout is not called
            assert is_authenticated == test_is_authenticated
            mock_logout.assert_not_called()
    

    @mock.patch.object(Auth, "logout")
    @mock.patch.object(Auth, "valid_until")
    def test_auth_is_authenticated__expired(self, mock_valid_until, mock_logout, random_user):
        # Given - we create a session with an expired time
        test_is_authenticated = False
        expired_minutes = SESSION_TIMEOUT_MINUTES * 2
        expired_valid_until = datetime_utcnow() - relativedelta(minutes=expired_minutes)
        mock_valid_until.return_value = expired_valid_until
        with app.test_request_context():
            Auth.create_session(random_user)
            
            # When - we check is_authenticated
            is_authenticated = Auth.is_authenticated()

            # Then - return false, logout is called
            assert is_authenticated == test_is_authenticated
            mock_logout.assert_called()


class TestAuthValidUntil:
    def test__auth_valid_until(self):
        # Given - we know the time and minutes to add
        frozen_datetime_utc = datetime(2023, 9, 1, 18, 9, 1)
        utc_offset = -4
        utc_timezone = pytz.timezone("UTC")
        test_valid_until = utc_timezone.localize(
            frozen_datetime_utc + relativedelta(minutes=SESSION_TIMEOUT_MINUTES)
        ).replace(tzinfo=None)
        with freeze_time(frozen_datetime_utc, utc_offset):
            # When - we request the valid_until date
            valid_until = Auth.valid_until()

            # Then - it matches our expectations
            assert valid_until == test_valid_until


class TestAuthGenerateUserToken:
    def test__auth_generate_token(self):
        # When - we generate a token
        token = Auth.generate_token()

        # Then - what we are expecting is returned
        assert token != None
        assert token != ""
        assert type(token) == str
        assert len(token) == 165


class TestAuthAuthenticateLoginToken:
    def test__auth_authenticate_login_token__user_not_found(self):
        # Given - we don't generate a user
        token = "invalid"
        # When - we pass an invalid token to be authenticated
        is_authenticated = Auth.authenticate_user_token(token)
        # Then - false is returned
        assert is_authenticated == False


class TestAuthAuthenticateLoginToken:
    def test__auth_authenticate_login_token__deactivated_user(self, token_user):
        # Given - we generate and deactivate a user with a login token
        token_user.date_deactivated = datetime_utcnow()
        db.session.add(token_user)
        db.session.commit()

        # When - we pass the correct token to be authenticated
        is_authenticated = Auth.authenticate_login_token(token_user.login_token)

        # Then - false is returned
        assert is_authenticated == False


    @mock.patch.object(Auth, "create_session")
    def test__auth_authenticate_login_token__valid(self, mock_create_session, token_user):
        # Given - we generate a user with a login token
        # When - we pass the correct token to be authenticated
        mock_create_session.return_value = True
        is_authenticated = Auth.authenticate_login_token(token_user.login_token)

        # Then - true is returned
        assert is_authenticated == True