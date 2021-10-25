import io

from rest_framework.test import APITestCase, APIClient

from authentication.enums import VolunteerVioState
from authentication.models import User
from report.models import DeforestationReport
from volunteer.models import Volunteer


class ReportIntegrationTests(APITestCase):
    def setUp(self) -> None:
        self.rest_client = APIClient()
        self.main_report_data = {
            "district": "Ampara",
            "severity": "5",
            "recent": "True",
            "action_description": "action card ",
            "special_notes": "I'm special",
        }

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
                "email": "volunteertest1@gmail.com",
                "password": "password"
            }

        }

        response = self.rest_client.post("/api/volunteer/register", data=self.main_volunteer_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(VolunteerVioState.UNAPPROVED, response.data["state"])
        _user = User.objects.get(email=response.data["user"]["email"])
        response = self.rest_client.post(f"/api/auth/email_verify/{_user.email_token}")
        self.assertTrue(response.data)
        self.rest_client.credentials()

        response = self.rest_client.post("/api/auth/login", data={
            "email": _user.email,
            "password": "password",
        })

        volunteer = Volunteer.objects.get(user=_user)
        volunteer.state = VolunteerVioState.APPROVED
        volunteer.save()

        self.assertEqual(response.status_code, 200)
        self.main_volunteer_token = response.data["token"]
        self.main_volunteer_id = response.data["id"]
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_volunteer_token)

        report_data = {**self.main_report_data, "long": 6.937, "lat": 79.273, "volunteer": volunteer}
        self.report1 = DeforestationReport.objects.create(**report_data)

    def test_create_report(self):
        with open('C:\\Users\\ACER\\OneDrive\\Pictures\\Screenshots\\2021-10-22.png', 'rb') as fp:
            fio = io.FileIO(fp.fileno())
            fio.name = 'file.txt'
            self.main_report_data["images"] = [fio]
            self.main_report_data["location"] = "Location man"
            response = self.rest_client.post("/api/reports/create", self.main_report_data)
            self.assertEqual(response.status_code, 201)

    def test_get_report_by_district(self):
        response = self.rest_client.get("/api/reports/Ampara")
        self.assertEqual(response.status_code, 200)

    def test_get_report_by_id(self):
        response = self.rest_client.get(f"/api/reports/get/{self.report1.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.report1.id)
