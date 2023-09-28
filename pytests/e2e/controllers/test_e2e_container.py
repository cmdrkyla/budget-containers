import json
from unittest import mock

from app import app
from auth.auth import Auth
from models.container import FrequencyMonthRepeat, FrequencyType

@mock.patch.object(Auth, "is_authenticated")
class TestContainerControllerCreateE2E:
    def test__container_controller_create(
            self, mock_auth_authenticate, user_with_records
        ):
        # Given - a container to add
        user = user_with_records["user"]
        container_data = {
            "amount": 10.01,
            "frequency_interval": 1,
            "frequency_month_repeat": FrequencyMonthRepeat.SAME_DATE.value,
            "frequency_type": FrequencyType.MONTH.value,
            "name": "Gas",
            "start_date": "2023-09-01",
            "user_id": user.id,
        }
        mock_auth_authenticate.return_value = True

        # When - we create the user
        response = app.test_client().post(
            "/api/container/create",
            data=json.dumps(container_data),
            content_type='application/json',
        )

        # Then - success status code and valid data
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert container_data["name"] == response_json["name"]


@mock.patch.object(Auth, "is_authenticated")
class TestContainerControllerReadE2E:
    def test__container_controller_read(self, mock_auth_authenticate, user_with_records):
        # Given - we have a user with container
        container_id = user_with_records["container"].id
        mock_auth_authenticate.return_value = True
        
        # When - we request to read that container record
        response = app.test_client().get(f"/api/container/read/{container_id}")
        
        # Then - success status code and valid data
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert container_id == int(response_json["id"])


@mock.patch.object(Auth, "is_authenticated")
class TestContainerControllerUpdateE2E:
    def test__container_controller_update(self, mock_auth_authenticate, user_with_records):
        # Given - a container to modify
        container_data = {"name": "Fuel", "start_date": "2023-09-02"}
        container_id = user_with_records["container"].id
        mock_auth_authenticate.return_value = True

        # When - we update the container
        response = app.test_client().put(
            f"/api/container/update/{container_id}",
            data=json.dumps(container_data),
            content_type='application/json',
        )

        # Then - success status code and valid data
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert container_data["name"] == response_json["name"]


@mock.patch.object(Auth, "is_authenticated")
class TestContainerControllerDeleteE2E:
    def test__container_controller_delete(self, mock_auth_authenticate, user_with_records):
        # Given - we have a container
        container_id = user_with_records["container"].id
        mock_auth_authenticate.return_value = True

        # When - we delete that record
        response = app.test_client().delete(f"/api/container/delete/{container_id}")

        # Then - success status code and deactivated date
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert response_json["deactivated_at"] != None


@mock.patch.object(Auth, "is_authenticated")
class TestContainerControllerListE2E:
    def test__container_controller_list(self, mock_auth_authenticate, user_with_records):
        # Given - we have a container
        container_id = user_with_records["container"].id
        mock_auth_authenticate.return_value = True

        # When - we list the records
        response = app.test_client().get(f"/api/container/list")
        
        # Then - success status code and valid data
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert len(response_json) == 1
        assert container_id == response_json[0]["id"]
