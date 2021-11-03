from rest_framework.test import APITestCase

from authentication.enums import UserType
from authentication.models import User
from helpers.token_generators import gen_email_token
from report.models import DeforestationReport
from volunteer.models import Volunteer


class TestReportModel(APITestCase):
    def setUp(self) -> None:
        self.main_report_data = {
            "title": "Plant trees in colombo",
            "district": "Ampara",
            "severity": "5",
            "long": 6.490,
            "lat": 79.349,
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
                "email": "volunter1@gmail.com",
                "password": "password"
            }

        }

        user_details = {
            **self.main_volunteer_data["user"],
            "user_type": UserType.VOLUNTEER,
            "email_token": gen_email_token(),
        }
        user = User.objects.create(**user_details)

        volunteer_details = {**self.main_volunteer_data, "user": user}

        volunteer = Volunteer.objects.create(**volunteer_details)
        self.main_report_data["volunteer"] = volunteer

    def test_create_report(self):
        report = DeforestationReport.objects.create(**self.main_report_data)
        self.assertEqual(report.severity, self.main_report_data["severity"])
        report.delete()

    """
        def test_create_report_image(self):
        report = DeforestationReport.objects.create(**self.main_report_data)
        self.assertEqual(report.severity, self.main_report_data["severity"])

        with open("C:\\Users\\ACER\\OneDrive\\Pictures\\Screenshots\\2021-10-22.png", "rb+") as f0:
            report_photo = ReportPhoto.objects.create(**{"image": f0, "report": report})
            self.assertEqual(report_photo.report.id, report.id)
    """
