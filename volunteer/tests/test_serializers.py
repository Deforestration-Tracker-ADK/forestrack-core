from rest_framework.test import APITestCase

from authentication.enums import UserType
from authentication.models import User
from helpers.token_generators import gen_email_token
from volunteer.models import Volunteer
from volunteer.serializers import VolunteerRegisterSerializer


class TestVolunteerSerializer(APITestCase):
    def setUp(self) -> None:
        self.serializer_class = VolunteerRegisterSerializer
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

    def test_serializer_validation_accept(self):
        serializer = self.serializer_class(data=self.main_volunteer_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_validation_dob_in_future(self):
        data = {
            **self.main_volunteer_data,
            "dob": "2098-04-05"
        }

        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_validation_contact_number_in_future(self):
        data = {
            **self.main_volunteer_data,
            "contactNumber": "0778489387854"
        }

        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_validation_nic_already_exist(self):
        user_details = {
            **self.main_volunteer_data["user"],
            "user_type": UserType.VOLUNTEER,
            "email_token": gen_email_token(),
        }
        user = User.objects.create(**user_details)

        volunteer_details = {**self.main_volunteer_data, "user": user}

        volunteer = Volunteer.objects.create(**volunteer_details)
        serializer = self.serializer_class(data=self.main_volunteer_data)
        self.assertFalse(serializer.is_valid())
        volunteer.delete()

    def test_serializer_create(self):
        serializer = self.serializer_class(data=self.main_volunteer_data)
        self.assertTrue(serializer.is_valid())
        volunteer = serializer.save()
        self.assertEqual(volunteer.nic, self.main_volunteer_data["nic"])
        self.assertEqual(volunteer.nameNIC, self.main_volunteer_data["nameNIC"])
