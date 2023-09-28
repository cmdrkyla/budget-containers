from decimal import Decimal
import json
from unittest import mock

from app import app
from auth.auth import Auth
from imports.functions import date_utcnow

@mock.patch.object(Auth, "is_authenticated")
class TestActivityControllerCreateE2E:
    def test__activity_controller_create(
            self, mock_auth_authenticate, user_with_records
        ):
        # Given - an activity to add
        user = user_with_records["user"]
        container = user_with_records["container"]
        period = user_with_records["period"]
        activity_data = {
            "activity_date": date_utcnow().strftime("%Y-%m-%d"),
            "amount": 10.01,
            "container_id": container.id,
            "period_id": period.id,
            "user_id": user.id,
        }
        mock_auth_authenticate.return_value = True

        # When - we create the user
        response = app.test_client().post(
            "/api/activity/create",
            data=json.dumps(activity_data),
            content_type='application/json',
        )

        # Then - success status code and valid data
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert activity_data["container_id"] == response_json["container_id"]


@mock.patch.object(Auth, "is_authenticated")
class TestActivityControllerReadE2E:
    def test__activity_controller_read(self, mock_auth_authenticate, user_with_activity):
        # Given - we have a user with activity
        activity_id = user_with_activity["activity"].id
        mock_auth_authenticate.return_value = True
        
        # When - we request to read that activity record
        response = app.test_client().get(f"/api/activity/read/{activity_id}")
        
        # Then - success status code and valid data
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert activity_id == int(response_json["id"])


@mock.patch.object(Auth, "is_authenticated")
class TestActivityControllerUpdateE2E:
    def test__activity_controller_update(self, mock_auth_authenticate, user_with_activity):
        # Given - an activity to modify
        activity_data = {"description": "Plato's Closet"}
        activity_id = user_with_activity["activity"].id
        mock_auth_authenticate.return_value = True

        # When - we update the activity
        response = app.test_client().put(
            f"/api/activity/update/{activity_id}",
            data=json.dumps(activity_data),
            content_type='application/json',
        )

        # Then - success status code and valid data
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert activity_data["description"] == response_json["description"]


@mock.patch.object(Auth, "is_authenticated")
class TestActivityControllerDeleteE2E:
    def test__activity_controller_delete(self, mock_auth_authenticate, user_with_activity):
        # Given - we have an activity
        activity_id = user_with_activity["activity"].id
        mock_auth_authenticate.return_value = True

        # When - we delete that record
        response = app.test_client().delete(f"/api/activity/delete/{activity_id}")

        # Then - success status code and deactivated date
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert response_json["deactivated_at"] != None


@mock.patch.object(Auth, "is_authenticated")
class TestActivityControllerListE2E:
    def test__activity_controller_list(self, mock_auth_authenticate, user_with_activity):
        # Given - we have an activity
        activity_id = user_with_activity["activity"].id
        mock_auth_authenticate.return_value = True

        # When - we list the records
        response = app.test_client().get(f"/api/activity/list")
        
        # Then - success status code and valid data
        assert response.status_code == 200
        response_json = json.loads(response.text)
        assert len(response_json) == 1
        assert activity_id == response_json[0]["id"]