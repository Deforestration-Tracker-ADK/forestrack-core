from rest_framework.test import APITestCase

from authentication.enums import UserType
from authentication.models import User
from helpers.token_generators import gen_email_token
from report.models import DeforestationReport
from report.services import ReportService
from volunteer.models import Volunteer


class TestReportService(APITestCase):
    def setUp(self) -> None:
        self.service = ReportService
        self.main_report_data = {
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
        self.report1 = DeforestationReport.objects.create(**self.main_report_data)
        self.report2 = DeforestationReport.objects.create(**self.main_report_data)

    def test_get_reports_with_image(self):
        reports = self.service.get_reports_with_image(self.report1.id)
        self.assertEqual(reports["district"], self.main_report_data["district"])

    def test_get_reports_without_images(self):
        reports = self.service.get_reports_without_images(self.main_report_data["district"])
        self.assertEqual(len(reports), 2)
        self.assertEqual(reports[0]["district"], self.main_report_data["district"])

        reports = self.service.get_reports_without_images(self.main_report_data["district"], 1)
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0]["district"], self.main_report_data["district"])
