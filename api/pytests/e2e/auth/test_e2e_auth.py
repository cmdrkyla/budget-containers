from unittest import mock

from app import app
from auth.auth import Auth

class TestAuthLogoutE2E:
    @mock.patch.object(Auth, "authenticate")
    def test__auth_logout(self, mock_auth_authenticate):
        # Given - we currently have a valid session (login)
        valid_email_address = "valid_email_address"
        valid_password = "valid_password"
        mock_auth_authenticate.return_value = True
        app.test_client().post(
            "/api/auth/login",
            data={
                "email_address": valid_email_address,
                "password": valid_password
            },
        )

        # When - we logout
        response = app.test_client().get("api/auth/logout")

        # Then - the session data is destroyed
        assert response.status_code == 200