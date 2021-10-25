from rest_framework.test import APITestCase, APIClient

from authentication.enums import VolunteerVioState
from authentication.models import User


class VolunteerIntegrationTests(APITestCase):
    def setUp(self) -> None:
        self.rest_client = APIClient()
        self.main_volunteer_data = {
            "first_name": "Devin",
            "last_name": "De Silva",
            "nic": "982970191v",
            "nameNIC": "D. Y. De Silva",
            "gender": "MALE",
            "dob": "1998-04-05",
            "address": "145/5 Salgas mawatha mattegoda",
            "district": "colombo",
            "preferredLanguage": "SINHALA",
            "highestEducation": "OL",
            "contactNumber": "077848938",
            "user": {
                "email": "volunter1@gmail.com",
                "password": "password"
            }

        }

        response = self.rest_client.post("/api/volunteer/register", data=self.main_volunteer_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(VolunteerVioState.UNAPPROVED, response.data["state"])
        _user = User.objects.get(email=response.data["user"]["email"])
        response = self.rest_client.post(f"/api/auth/email_verify/{_user.email_token}")
        self.assertTrue(response.data)
        response = self.rest_client.post("/api/auth/login", data={
            "email": self.main_volunteer_data["user"]["email"],
            "password": self.main_volunteer_data["user"]["password"]
        })

        self.assertEqual(response.status_code, 200)
        self.main_volunteer_token = response.data["token"]
        self.main_volunteer_id = response.data["id"]
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_volunteer_token)

    def test_auth_volunteer(self):
        response = self.rest_client.get("/api/volunteer/view")
        self.assertEqual(response.status_code, 200)

    def test_get_unapproved_volunteer(self):
        response = self.rest_client.get("/api/volunteer/unapproved")
        self.assertEqual(len(response.data), 1)

    def test_get_volunteer_by_id(self):
        response = self.rest_client.get(f"/api/volunteer/get/{self.main_volunteer_id}")
        self.assertEqual(response.data["nic"], self.main_volunteer_data["nic"])
