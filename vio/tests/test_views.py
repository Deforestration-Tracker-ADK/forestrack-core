from rest_framework.test import APITestCase, APIClient

from authentication.enums import VolunteerVioState
from authentication.models import User


class VioIntegrationTests(APITestCase):
    def setUp(self) -> None:
        self.rest_client = APIClient()
        self.main_vio_data = {
            "name": "Ocean warriors",
            "description": "Ocean willl look amazing in the future and we will be apart of it",
            "registrationNo": "98210kofne",
            "address": "145/5 Salgas mawatha mattegoda",
            "contactNumber": "0722334670",
            "registrationDate": "2017-10-12",
            "district": "colombo",
            "user": {
                "email": "vio1@gmail.com",
                "password": "password"
            }

        }

        response = self.rest_client.post("/api/vio/register", data=self.main_vio_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(VolunteerVioState.UNAPPROVED, response.data["state"])
        _user = User.objects.get(email=response.data["user"]["email"])
        response = self.rest_client.post(f"/api/auth/email_verify/{_user.email_token}")
        self.assertTrue(response.data)
        response = self.rest_client.post("/api/auth/login", data={
            "email": self.main_vio_data["user"]["email"],
            "password": self.main_vio_data["user"]["password"]
        })

        self.assertEqual(response.status_code, 200)
        self.main_volunteer_token = response.data["token"]
        self.main_volunteer_id = response.data["id"]
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_volunteer_token)

    def test_auth_vio(self):
        response = self.rest_client.get("/api/vio/view")
        self.assertEqual(response.status_code, 200)

    def test_get_unapproved_vio(self):
        response = self.rest_client.get("/api/vio/unapproved")
        self.assertEqual(len(response.data), 1)

    def test_get_vio_by_id(self):
        response = self.rest_client.get(f"/api/vio/get/{self.main_volunteer_id}")
        self.assertEqual(response.data["registrationNo"], self.main_vio_data["registrationNo"])
