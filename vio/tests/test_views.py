from rest_framework.test import APITestCase, APIClient

from authentication.enums import VolunteerVioState, UserState, UserType
from authentication.models import User
from helpers.token_generators import gen_email_token
from opportunity.enums import OpportunityState, VolunteerOpportunityState
from opportunity.models import Opportunity, VolunteerOpportunity
from vio.models import Vio
from volunteer.models import Volunteer


class VioIntegrationTests(APITestCase):
    def setUp(self) -> None:
        self.rest_client = APIClient()
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

        response = self.rest_client.post("/api/vio/register", data=self.main_vio_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(VolunteerVioState.UNAPPROVED, response.data["state"])
        _user = User.objects.get(email=response.data["user"]["email"])
        response = self.rest_client.post(f"/api/auth/email_verify/{_user.email_token}")
        self.assertTrue(response.data)
        response = self.rest_client.post("/api/auth/login", data={
            "email": self.main_vio_data["user"]["email"],
            "password": self.main_vio_data["user"]["password"]
        })

        self.assertEqual(response.status_code, 200)
        self.main_vio_token = response.data["token"]
        self.main_vio_id = response.data["id"]
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_vio_token)

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

    def test_register_already_vio(self):
        response = self.rest_client.post("/api/vio/register", data=self.main_vio_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_accept_volunteer_for_opportunity(self):
        vio = Vio.objects.get(user_id=self.main_vio_id)
        vio.state = VolunteerVioState.APPROVED
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
            "vio_id": self.main_vio_id,
        }

        opportunity_approved = Opportunity.objects.create(**self.main_opportunity_data_approved)
        opportunity_approved.state = OpportunityState.APPROVED
        opportunity_approved.save()
        self.opportunity_approved = opportunity_approved

        self.volunteer_opportunity = VolunteerOpportunity.objects.create(**{
            "volunteer_id": self.volunteer.user_id,
            "opportunity_id": self.opportunity_approved.id
        })

        response = self.rest_client.post("/api/vio/approve/volunteer", data={
            "approve": True,
            "vol_opp_id": self.volunteer_opportunity.id
        }, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Volunteer has been approved")

        self.volunteer_opportunity = VolunteerOpportunity.objects.get(id=self.volunteer_opportunity.id)
        self.volunteer_opportunity.state = VolunteerOpportunityState.PENDING
        self.volunteer_opportunity.save()

        response = self.rest_client.post("/api/vio/approve/volunteer", data={
            "approve": False,
            "vol_opp_id": self.volunteer_opportunity.id
        }, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Volunteer has been rejected")

    def test_auth_vio(self):
        response = self.rest_client.get("/api/vio/view")
        self.assertEqual(response.status_code, 200)

    def test_get_unapproved_vio(self):
        response = self.rest_client.get("/api/vio/unapproved")
        self.assertEqual(len(response.data), 1)

    def test_get_vio_by_id(self):
        response = self.rest_client.get(f"/api/vio/get/{self.main_vio_id}")
        self.assertEqual(response.data["registrationNo"], self.main_vio_data["registrationNo"])
