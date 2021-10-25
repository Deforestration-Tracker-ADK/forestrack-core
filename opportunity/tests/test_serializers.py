from rest_framework.test import APITestCase

from authentication.enums import UserType, UserState, VolunteerVioState
from authentication.models import User
from helpers.token_generators import gen_email_token
from opportunity.enums import OpportunityState
from opportunity.models import Opportunity
from opportunity.serializers import OpportunitySerializer, ApplyForOpportunitySerializer
from vio.models import Vio
from volunteer.models import Volunteer


class TestOpportunitySerializer(APITestCase):
    def setUp(self) -> None:
        self.serializer_class = OpportunitySerializer
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

        user_details = {
            **self.main_vio_data["user"],
            "user_type": UserType.VIO,
            "email_token": gen_email_token(),
        }
        user = User.objects.create(**user_details)
        vio_details = {**self.main_vio_data, "user": user}
        vio = Vio.objects.create(**vio_details)
        user.state = UserState.EMAIL_VERIFIED
        vio.state = VolunteerVioState.APPROVED
        user.save()
        vio.save()

        self.main_opportunity_data = {
            "name": "Shramadhana at Sinharaja.",
            "description": "Shramadhana at sinharaja forest resovior",
            "address": "address to gether together",
            "district": "district of the Shramadhana",
            "start_date": "2021-11-25",
            "end_date": "2021-11-30",
            "goals": "The sharamadhana is organized to make the sharamadhana to protect earth",
            "contactPersonNumber": "0776685899",
            "numVolunteers": 3,
            "vio_id": vio.user_id,
        }

    def test_serializer_validation_accept(self):
        serializer = self.serializer_class(data=self.main_opportunity_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_validation_start_date_in_future(self):
        data = {
            **self.main_opportunity_data,
            "start_date": "2021-10-14"
        }

        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_validation_end_date_in_future(self):
        data = {
            **self.main_opportunity_data,
            "end_date": "2021-10-14"
        }

        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_validation_start_date_in_future_end_date(self):
        data = {
            **self.main_opportunity_data,
            "start_date": "2021-11-20",
            "end_date": "2021-10-30"
        }

        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_validation_no_user_exist(self):
        data = {
            **self.main_opportunity_data,
            "vio_id": 5
        }

        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_create(self):
        serializer = self.serializer_class(data=self.main_opportunity_data)
        self.assertTrue(serializer.is_valid())
        opportunity = serializer.save()
        self.assertEqual(opportunity.name, self.main_opportunity_data["name"])
        self.assertEqual(opportunity.district, self.main_opportunity_data["district"])


class TestVolunteerOpportunitySerializer(APITestCase):
    def setUp(self) -> None:
        self.serializer_class = ApplyForOpportunitySerializer
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

        user_details = {
            **self.main_vio_data["user"],
            "user_type": UserType.VIO,
            "email_token": gen_email_token(),
        }
        user = User.objects.create(**user_details)
        vio_details = {**self.main_vio_data, "user": user}
        vio = Vio.objects.create(**vio_details)
        user.state = UserState.EMAIL_VERIFIED
        vio.state = VolunteerVioState.APPROVED
        user.save()
        vio.save()

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
        user.state = UserState.EMAIL_VERIFIED
        volunteer.state = VolunteerVioState.APPROVED
        user.save()
        volunteer.save()
        self.volunteer = volunteer

        self.main_opportunity_data = {
            "name": "Shramadhana at Sinharaja.",
            "description": "Shramadhana at sinharaja forest resovior",
            "address": "address to gether together",
            "district": "district of the Shramadhana",
            "start_date": "2021-10-25",
            "end_date": "2021-10-30",
            "goals": "The sharamadhana is organized to make the sharamadhana to protect earth",
            "contactPersonNumber": "0776685899",
            "numVolunteers": 3,
            "vio_id": vio.user_id,
        }

        opportunity = Opportunity.objects.create(**self.main_opportunity_data)
        opportunity.state = OpportunityState.APPROVED
        opportunity.save()
        self.opportunity = opportunity

    def test_serializer_validation_pass(self):
        data = {
            "volunteer_id": self.volunteer.user_id,
            "opportunity_id": self.opportunity.id
        }

        serializer = self.serializer_class(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_validation_no_such_volunteer_error(self):
        data = {
            "volunteer_id": 10,
            "opportunity_id": self.opportunity.id
        }

        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_validation_no_such_opportunity_error(self):
        data = {
            "volunteer_id": self.volunteer.user_id,
            "opportunity_id": 10
        }

        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_volunteer_opportunity_exist(self):
        data = {
            "volunteer_id": self.volunteer.user_id,
            "opportunity_id": self.opportunity.id
        }

        serializer = self.serializer_class(data=data)
        self.assertTrue(serializer.is_valid())
        vol_opp = serializer.save()
        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())
        vol_opp.delete()

    def test_serializer_volunteer_opportunity_create(self):
        data = {
            "volunteer_id": self.volunteer.user_id,
            "opportunity_id": self.opportunity.id
        }

        serializer = self.serializer_class(data=data)
        self.assertTrue(serializer.is_valid())
        vol_opp = serializer.save()
        self.assertEqual(vol_opp.volunteer_id, data["volunteer_id"])
        self.assertEqual(vol_opp.opportunity_id, data["opportunity_id"])
