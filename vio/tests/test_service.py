from rest_framework.test import APITestCase

from authentication.enums import VolunteerVioState, UserType, UserState
from authentication.models import User
from helpers.token_generators import gen_email_token
from opportunity.enums import OpportunityState, VolunteerOpportunityState
from opportunity.models import Opportunity, VolunteerOpportunity
from vio.serializers import VioRegisterSerializer
from vio.services import VioService
from volunteer.models import Volunteer


class TestVioService(APITestCase):
    def setUp(self) -> None:
        self.serializer_class = VioRegisterSerializer
        self.service = VioService
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

        vio1_serializer = self.serializer_class(data=self.main_vio_data)
        self.assertTrue(vio1_serializer.is_valid())
        self.vio1 = vio1_serializer.save()
        self.vio1.state = VolunteerVioState.APPROVED
        user = User.objects.get(id=self.vio1.user_id)
        user.state = UserState.EMAIL_VERIFIED
        user.save()
        self.vio1.save()

        vio2_data = {
            **self.main_vio_data,
            "registrationNo": "982970767v",
            "user": {
                "email": "vio2@gmail.com",
                "password": "password"
            }
        }

        vio2_serializer = self.serializer_class(data=vio2_data)
        self.assertTrue(vio2_serializer.is_valid())
        self.vio2 = vio2_serializer.save()

        vol3_data = {
            **self.main_vio_data,
            "registrationNo": "982767767v",
            "user": {
                "email": "vio3@gmail.com",
                "password": "password"
            }
        }

        vio3_serializer = self.serializer_class(data=vol3_data)
        self.assertTrue(vio3_serializer.is_valid())
        self.vio3 = vio3_serializer.save()

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

        self.main_opportunity_data_approved = {
            "name": "approved opportunity",
            "description": "Shramadhana at sinharaja forest resovior",
            "address": "address to gether together",
            "district": "district of the Shramadhana",
            "start_date": "2021-10-25",
            "end_date": "2021-10-30",
            "goals": "The sharamadhana is organized to make the sharamadhana to protect earth",
            "contactPersonNumber": "0776685899",
            "numVolunteers": 3,
            "vio_id": self.vio1.user_id,
        }

        opportunity_approved = Opportunity.objects.create(**self.main_opportunity_data_approved)
        opportunity_approved.state = OpportunityState.APPROVED
        opportunity_approved.save()
        self.opportunity_approved = opportunity_approved

        self.volunteer_opportunity = VolunteerOpportunity.objects.create(**{
            "volunteer_id": self.volunteer.user_id,
            "opportunity_id": self.opportunity_approved.id
        })

    def test_getVio(self):
        vio = self.service.getVio(state=VolunteerVioState.UNAPPROVED)
        self.assertEqual(len(vio), 2)
        self.assertEqual(vio[0]["description"], self.main_vio_data["description"])

        vio = self.service.getVio(state=VolunteerVioState.UNAPPROVED, num_of=2)
        self.assertEqual(len(vio), 2)
        self.assertEqual(vio[0]["description"], self.main_vio_data["description"])

    def test_getVioById(self):
        vio = self.service.getVioById(self.vio2.user_id)
        self.assertEqual("Ocean willl look amazing in the future and we will be apart of it", vio["description"])

        vio = self.service.getVioById(self.vio1.user_id)
        self.assertEqual("vio1@gmail.com", vio["user"]["email"])

    def test_approveVolunteerForOpportunity(self):
        user = User.objects.get(id=self.vio1.user_id)
        is_approved = self.service.approveVolunteerForOpportunity(self.volunteer_opportunity.id, True, user)
        self.assertTrue(is_approved)
        self.assertEqual(VolunteerOpportunity.objects.get(id=self.volunteer_opportunity.id).state,
                         VolunteerOpportunityState.ACCEPTED)

        self.volunteer_opportunity = VolunteerOpportunity.objects.get(id=self.volunteer_opportunity.id)
        self.volunteer_opportunity.state = VolunteerOpportunityState.PENDING
        self.volunteer_opportunity.save()

        is_rejected = self.service.approveVolunteerForOpportunity(self.volunteer_opportunity.id, False, user)
        self.assertTrue(is_rejected)
        self.assertEqual(VolunteerOpportunity.objects.get(id=self.volunteer_opportunity.id).state,
                         VolunteerOpportunityState.REJECTED)

        user = User.objects.get(id=self.vio2.user_id)
        self.volunteer_opportunity = VolunteerOpportunity.objects.get(id=self.volunteer_opportunity.id)
        self.volunteer_opportunity.state = VolunteerOpportunityState.PENDING
        self.volunteer_opportunity.save()

        is_rejected = self.service.approveVolunteerForOpportunity(self.volunteer_opportunity.id, True, user)
        self.assertFalse(is_rejected)

        is_rejected = self.service.approveVolunteerForOpportunity(10, True, user)
        self.assertFalse(is_rejected)
