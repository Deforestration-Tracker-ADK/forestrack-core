from rest_framework.test import APITestCase

from authentication.enums import UserType, UserState, VolunteerVioState
from authentication.models import User
from helpers.token_generators import gen_email_token
from opportunity.enums import OpportunityState, VolunteerOpportunityState
from opportunity.models import Opportunity, VolunteerOpportunity
from opportunity.serializers import OpportunitySerializer
from opportunity.services import OpportunityService
from vio.models import Vio
from volunteer.models import Volunteer


class TestOpportunityService(APITestCase):
    def setUp(self) -> None:
        self.serializer_class = OpportunitySerializer
        self.service = OpportunityService
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
        self.vio = vio
        vio.save()

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
            "vio_id": vio.user_id,
        }

        opportunity_approved = Opportunity.objects.create(**self.main_opportunity_data_approved)
        opportunity_approved.state = OpportunityState.APPROVED
        opportunity_approved.save()
        self.opportunity_approved = opportunity_approved

        self.main_opportunity_data_unapproved = {
            **self.main_opportunity_data_approved,
            "name": "unapproved opportunity"
        }

        Opportunity.objects.create(**self.main_opportunity_data_unapproved)
        self.opportunity_unapproved = Opportunity.objects.create(**self.main_opportunity_data_unapproved)

        self.main_opportunity_data_complete = {
            **self.main_opportunity_data_approved,
            "name": "complete opportunity"
        }

        self.opportunity_complete = Opportunity.objects.create(**self.main_opportunity_data_complete)
        self.opportunity_complete.state = OpportunityState.COMPLETED
        self.opportunity_complete.save()

        self.volunteer_opportunity = VolunteerOpportunity.objects.create(**{
            "volunteer_id": self.volunteer.user_id,
            "opportunity_id": self.opportunity_approved.id
        })

    def test_getVolunteerOpportunitiesFromId(self):
        vol_opp = self.service.getVolunteerOpportunitiesFromId(self.volunteer_opportunity.id)
        self.assertTrue(vol_opp["id"], self.volunteer_opportunity.id)

    def test_complete_opportunity(self):
        opportunity_data = {
            "name": "test complete this opportunity",
            "description": "Shramadhana",
            "address": "address to ",
            "district": "district of thea",
            "start_date": "2021-10-25",
            "end_date": "2021-10-30",
            "goals": "The sharamade the sharamadhana to protect earth",
            "contactPersonNumber": "0776685899",
            "numVolunteers": 6,
            "vio_id": self.vio.user_id,
        }

        opportunity_approved = Opportunity.objects.create(**opportunity_data)
        opportunity_approved.state = OpportunityState.APPROVED
        opportunity_approved.save()

        opportunity = self.service.completeOpportunity(opportunity_approved.id, self.vio.user)
        self.assertTrue(opportunity)

    def test_opportunities(self):
        opportunities = self.service.getOpportunities(state=OpportunityState.UNAPPROVED)
        self.assertEqual(len(opportunities), 2)

        opportunities = self.service.getOpportunities(state=OpportunityState.UNAPPROVED, num_of=1)
        self.assertEqual(len(opportunities), 1)

    def test_getVolunteerOpportunitiesForVolunteer(self):
        vol_opp_list = self.service.getVolunteerOpportunitiesForVolunteer(self.volunteer.user_id,
                                                                          state=VolunteerOpportunityState.PENDING)
        self.assertEqual(len(vol_opp_list), 1)

        vol_opp_list = self.service.getVolunteerOpportunitiesForVolunteer(self.volunteer.user_id,
                                                                          state=VolunteerOpportunityState.PENDING,
                                                                          num_of=1)
        self.assertEqual(len(vol_opp_list), 1)

    def test_getVolunteerOpportunitiesForOpportunity(self):
        vol_opp_list = self.service.getVolunteerOpportunitiesForOpportunity(self.volunteer_opportunity.opportunity_id,
                                                                            state=VolunteerOpportunityState.PENDING)
        self.assertEqual(len(vol_opp_list), 1)

        vol_opp_list = self.service.getVolunteerOpportunitiesForOpportunity(self.volunteer_opportunity.opportunity_id,
                                                                            state=VolunteerOpportunityState.PENDING,
                                                                            num_of=1)
        self.assertEqual(len(vol_opp_list), 1)

    def test_getOpportunityById(self):
        opportunity = self.service.getOpportunityById(self.opportunity_complete.id)
        self.assertEqual(opportunity["id"], self.opportunity_complete.id)

    def test_getOpportunityByVioId(self):
        opportunity = self.service.getOpportunityByVioId(self.vio.user_id)
        self.assertEqual(len(opportunity), 1)

    def test_getOpportunitiesForVio(self):
        opportunity = self.service.getOpportunitiesForVio(self.vio.user_id, OpportunityState.COMPLETED)
        self.assertEqual(len(opportunity), 1)
