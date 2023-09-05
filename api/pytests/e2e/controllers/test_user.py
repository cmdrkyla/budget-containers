from unittest import mock

from app import app
from auth.auth import Auth
from controllers.user import UserController
from models.user import User

@mock.patch.object(Auth, "is_authenticated")
class TestUserControllerCreateE2E:
    def test__user_controller_create(self, mock_auth_authenticate):
        pass
        """
        # Given - a user to add
        user_data = {
            "email_address": "create_user@company.test",
            "name_first": "Create",
            "name_last": "User",
            "password": "CreateUserPassword",
        }
        mock_auth_authenticate.return_value = True

        # When - we login
        response = app.test_client().post(
            "/api/user/create",
            data=user_data,
        )

        # Then - success status code
        assert response.status_code == 200
        """