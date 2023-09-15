import json
from unittest import mock

from app import app
from auth.auth import Auth
from controllers.user import UserController
from models.user import User

@mock.patch.object(Auth, "is_authenticated")
class TestUserControllerCreateE2E:
    def test__user_controller_create(self, mock_auth_authenticate):
        # Given - a user to add
        user_data = {
            "email_address": "create_user@company.test",
            "name_first": "Create",
            "name_last": "User",
            "password": "CreateUserPassword",
        }
        mock_auth_authenticate.return_value = True

        # When - we create the user
        response = app.test_client().post(
            "/api/user/create",
            data=user_data,
        )

        # Then - success status code and valid data
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert user_data["email_address"] == response_json["email_address"]


@mock.patch.object(Auth, "is_authenticated")
class TestUserControllerReadE2E:
    def test__user_controller_read(self, mock_auth_authenticate, random_user):
        # Given - we have a random user
        mock_auth_authenticate.return_value = True

        # When - we request to read that user record
        response = app.test_client().get(f"/api/user/read/{random_user.id}")

        # Then - success status code and valid data
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert random_user.email_address == response_json["email_address"]


@mock.patch.object(Auth, "is_authenticated")
class TestUserControllerUpdateE2E:
    def test__user_controller_update(self, mock_auth_authenticate, random_user):
        # Given - a user to modify
        user_data = {
            "name_first": "New",
            "name_last": "Name",
        }
        mock_auth_authenticate.return_value = True

        # When - we update the user
        response = app.test_client().put(
            f"/api/user/update/{random_user.id}",
            data=user_data,
        )

        # Then - success status code and valid data
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert user_data["name_first"] == response_json["name_first"]


@mock.patch.object(Auth, "is_authenticated")
class TestUserControllerDeleteE2E:
    def test__user_controller_delete(self, mock_auth_authenticate, random_user):
        # Given - we have a random user
        mock_auth_authenticate.return_value = True

        # When - we delete that record
        response = app.test_client().delete(f"/api/user/delete/{random_user.id}")

        # Then - success status code and deactivated date
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert response_json["deactivated_at"] != None


@mock.patch.object(Auth, "is_authenticated")
class TestUserControllerListE2E:
    def test__user_controller_list(self, mock_auth_authenticate, random_user):
        # Given - we have a random user
        mock_auth_authenticate.return_value = True

        # When - we list the records
        response = app.test_client().get(f"/api/user/list")
        
        # Then - success status code and valid data
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert len(response_json) == 1
        assert random_user.email_address == response_json[0]["email_address"]