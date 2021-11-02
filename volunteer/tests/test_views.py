from rest_framework.test import APITestCase, APIClient

from authentication.enums import VolunteerVioState, UserType, UserState
from authentication.models import User
from helpers.token_generators import gen_email_token
from opportunity.enums import OpportunityState
from opportunity.models import Opportunity
from vio.models import Vio
from volunteer.models import Volunteer


class VolunteerIntegrationTests(APITestCase):
    def setUp(self) -> None:
        self.rest_client = APIClient()
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

        response = self.rest_client.post("/api/volunteer/register", data=self.main_volunteer_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(VolunteerVioState.UNAPPROVED, response.data["state"])
        _user = User.objects.get(email=response.data["user"]["email"])
        response = self.rest_client.post(f"/api/auth/email_verify/{_user.email_token}")
        self.assertTrue(response.data)
        response = self.rest_client.post("/api/auth/login", data={
            "email": self.main_volunteer_data["user"]["email"],
            "password": self.main_volunteer_data["user"]["password"]
        })

        self.assertEqual(response.status_code, 200)
        self.main_volunteer_token = response.data["token"]
        self.main_volunteer_id = response.data["id"]
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_volunteer_token)

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
        self.vio = vio

    def test_apply_for_opportunity(self):
        vol = Volunteer.objects.get(user_id=self.main_volunteer_id)
        vol.state = VolunteerVioState.APPROVED
        vol.save()

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
            "vio_id": self.vio.user_id,
        }

        opportunity_approved = Opportunity.objects.create(**self.main_opportunity_data_approved)
        opportunity_approved.state = OpportunityState.APPROVED
        opportunity_approved.save()
        self.opportunity_approved = opportunity_approved

        response = self.rest_client.post("/api/volunteer/opportunity/apply", data={
            "opportunity_id": self.opportunity_approved.id
        }, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["opportunity_id"], self.opportunity_approved.id)

    def test_auth_volunteer(self):
        response = self.rest_client.get("/api/volunteer/view")
        self.assertEqual(response.status_code, 200)

    def test_get_unapproved_volunteer(self):
        response = self.rest_client.get("/api/volunteer/unapproved")
        self.assertEqual(len(response.data), 1)

    def test_get_volunteer_by_id(self):
        response = self.rest_client.get(f"/api/volunteer/get/{self.main_volunteer_id}")
        self.assertEqual(response.data["nic"], self.main_volunteer_data["nic"])
