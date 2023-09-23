import json
from unittest import mock

from app import app
from auth.auth import Auth

@mock.patch.object(Auth, "is_authenticated")
class TestPeriodControllerCreateE2E:
    def test__period_controller_create(
            self, mock_auth_authenticate, user_with_records
        ):
        # Given - a period to add
        user = user_with_records["user"]
        period_data = {
            "start_date": "2023-09-01",
            "stop_date": "2023-09-30",
            "user_id": user.id,
        }
        mock_auth_authenticate.return_value = True

        # When - we create the user
        response = app.test_client().post(
            "/api/period/create",
            data=period_data,
        )

        # Then - success status code and valid data
        assert response.status_code == 200
        response_json = json.loads(response.text)
        # TODO: assert period_data["start_date"] == response_json["start_date"]


@mock.patch.object(Auth, "is_authenticated")
class TestPeriodControllerReadE2E:
    def test__period_controller_read(self, mock_auth_authenticate, user_with_records):
        # Given - we have a user with period
        period_id = user_with_records["period"].id
        mock_auth_authenticate.return_value = True
        
        # When - we request to read that period record
        response = app.test_client().get(f"/api/period/read/{period_id}")
        
        # Then - success status code and valid data
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert period_id == int(response_json["id"])


@mock.patch.object(Auth, "is_authenticated")
class TestPeriodControllerUpdateE2E:
    def test__period_controller_update(self, mock_auth_authenticate, user_with_records):
        # Given - a period to modify
        period_data = {"start_date": "2023-08-01"}
        period_id = user_with_records["period"].id
        mock_auth_authenticate.return_value = True

        # When - we update the period
        response = app.test_client().put(
            f"/api/period/update/{period_id}",
            data=period_data,
        )

        # Then - success status code and valid data
        assert response.status_code == 200
        response_json = json.loads(response.text)
        # TODO: assert period_data["start_date"] == response_json["start_date"]


@mock.patch.object(Auth, "is_authenticated")
class TestPeriodControllerDeleteE2E:
    def test__period_controller_delete(self, mock_auth_authenticate, user_with_records):
        # Given - we have a period
        period_id = user_with_records["period"].id
        mock_auth_authenticate.return_value = True

        # When - we delete that record
        response = app.test_client().delete(f"/api/period/delete/{period_id}")

        # Then - success status code and deactivated date
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert response_json["deactivated_at"] != None


@mock.patch.object(Auth, "is_authenticated")
class TestPeriodControllerListE2E:
    def test__period_controller_list(self, mock_auth_authenticate, user_with_records):
        # Given - we have a period
        period_id = user_with_records["period"].id
        mock_auth_authenticate.return_value = True

        # When - we list the records
        response = app.test_client().get(f"/api/period/list")
        
        # Then - success status code and valid data
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert len(response_json) == 1
        assert period_id == response_json[0]["id"]
