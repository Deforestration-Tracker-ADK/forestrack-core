from rest_framework.test import APITestCase

from authentication.enums import VolunteerVioState
from volunteer.serializers import VolunteerRegisterSerializer
from volunteer.services import VolunteerService


class TestVolunteerService(APITestCase):
    def setUp(self) -> None:
        self.serializer_class = VolunteerRegisterSerializer
        self.service = VolunteerService

        # create volunteer 1
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

        vol1_serializer = self.serializer_class(data=self.main_volunteer_data)
        self.assertTrue(vol1_serializer.is_valid())
        self.volunteer1 = vol1_serializer.save()

        # create volunteer 2
        vol2_data = {
            **self.main_volunteer_data,
            "nic": "982970767v",
            "user": {
                "email": "volunter2@gmail.com",
                "password": "password"
            }
        }

        vol2_serializer = self.serializer_class(data=vol2_data)
        self.assertTrue(vol2_serializer.is_valid())
        self.volunteer2 = vol2_serializer.save()

        # create volunteer 3
        vol3_data = {
            **self.main_volunteer_data,
            "nic": "982767767v",
            "user": {
                "email": "volunter3@gmail.com",
                "password": "password"
            }
        }

        vol3_serializer = self.serializer_class(data=vol3_data)
        self.assertTrue(vol3_serializer.is_valid())
        self.volunteer3 = vol3_serializer.save()

    def test_getVolunteer(self):
        """
        Testing getting volunteer List
        :return:
        """
        volunteer = self.service.getVolunteer(state=VolunteerVioState.UNAPPROVED)
        self.assertEqual(len(volunteer), 3)
        self.assertEqual(volunteer[0]["nameNIC"], self.main_volunteer_data["nameNIC"])

        volunteer = self.service.getVolunteer(state=VolunteerVioState.UNAPPROVED, num_of=2)
        self.assertEqual(len(volunteer), 2)
        self.assertEqual(volunteer[0]["nameNIC"], self.main_volunteer_data["nameNIC"])

    def test_getVolunteerById(self):
        """
        Testing getting a volunteer 
        :return:
        """
        volunteer = self.service.getVolunteerById(self.volunteer2.user_id)
        self.assertEqual("D. Y. De Silva", volunteer["nameNIC"])

        volunteer = self.service.getVolunteerById(self.volunteer1.user_id)
        self.assertEqual("volunter1@gmail.com", volunteer["user"]["email"])
