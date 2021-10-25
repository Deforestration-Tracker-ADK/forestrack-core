from rest_framework.test import APITestCase

from authentication.enums import UserType
from authentication.models import User
from helpers.token_generators import gen_email_token
from volunteer.models import Volunteer


class TestVolunteerModel(APITestCase):
    def setUp(self) -> None:
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

    def test_create_volunteer(self):
        user_details = {
            **self.main_volunteer_data["user"],
            "user_type": UserType.VOLUNTEER,
            "email_token": gen_email_token(),
        }
        user = User.objects.create(**user_details)

        volunteer_details = {**self.main_volunteer_data, "user": user}

        volunteer = Volunteer.objects.create(**volunteer_details)

        self.assertEqual(volunteer.nic, self.main_volunteer_data["nic"])
        self.assertEqual(volunteer.nameNIC, self.main_volunteer_data["nameNIC"])
        volunteer.delete()
        user.delete()
