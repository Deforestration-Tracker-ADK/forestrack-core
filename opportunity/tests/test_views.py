from rest_framework.test import APITestCase, APIClient

from authentication.enums import VolunteerVioState
from authentication.models import User
from opportunity.enums import OpportunityState
from opportunity.models import Opportunity, VolunteerOpportunity
from vio.models import Vio
from volunteer.models import Volunteer


class OpportunityIntegrationTest(APITestCase):
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
        vio = Vio.objects.get(user_id=_user.id)
        vio.state = VolunteerVioState.APPROVED
        vio.save()
        self.vio = vio
        self.assertTrue(response.data)

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
        volunteer = Volunteer.objects.get(user_id=_user.id)
        volunteer.state = VolunteerVioState.APPROVED
        volunteer.save()
        self.volunteer = volunteer
        self.assertTrue(response.data)

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

        response = self.rest_client.post("/api/auth/login", data={**self.main_vio_data["user"]})

        self.assertEqual(response.status_code, 200)
        self.main_vio_token = response.data["token"]
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_vio_token)

        response = self.rest_client.post("/api/auth/login", data={**self.main_volunteer_data["user"]})

        self.assertEqual(response.status_code, 200)
        self.main_volunteer_token = response.data["token"]

    def test_GetUnapprovedOpportunity(self):
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_vio_token)
        response = self.rest_client.get("/api/opportunity/approved")
        self.assertEqual(response.status_code, 200)

    def test_GetApprovedOpportunity(self):
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_vio_token)
        response = self.rest_client.get("/api/opportunity/get/unapproved")
        self.assertEqual(response.status_code, 200)

    def test_get_opportunity_by_id(self):
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_vio_token)
        response = self.rest_client.get(f"/api/opportunity/getOpportunity/{self.opportunity_approved.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.id, self.opportunity_approved.id)

    def test_get_opportunity_by_id(self):
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_vio_token)
        response = self.rest_client.get(f"/api/opportunity/getOpportunity/{self.opportunity_approved.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.opportunity_approved.id)

    def test_get_opportunities_unaccepted_for_vio(self):
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_vio_token)
        response = self.rest_client.get(f"/api/opportunity/vio/unaccepted/{self.vio.user_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_opportunities_approved_for_vio(self):
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_vio_token)
        response = self.rest_client.get(f"/api/opportunity/vio/approved/{self.vio.user_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_opportunities_completed_for_vio(self):
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_vio_token)
        response = self.rest_client.get(f"/api/opportunity/vio/completed/{self.vio.user_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_opportunities_for_vio(self):
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_vio_token)
        response = self.rest_client.get(f"/api/opportunity/vio/{self.vio.user_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_volunteer_opportunities_for_pending_volunteer(self):
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_volunteer_token)
        response = self.rest_client.get(f"/api/opportunity/volunteer/pending/{self.volunteer.user_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_volunteer_opportunities_for_completed_volunteer(self):
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_volunteer_token)
        response = self.rest_client.get(f"/api/opportunity/volunteer/completed/{self.volunteer.user_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_volunteer_opportunities_for_pending_opportunity(self):
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_volunteer_token)
        response = self.rest_client.get(
            f"/api/opportunity/pending/volunteers/{self.volunteer_opportunity.opportunity_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_volunteer_opportunities_for_accepted_opportunity(self):
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_volunteer_token)
        response = self.rest_client.get(
            f"/api/opportunity/accepted/volunteers/{self.volunteer_opportunity.opportunity_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_volunteer_opportunities_for_completed_opportunity(self):
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_volunteer_token)
        response = self.rest_client.get(
            f"/api/opportunity/completed/volunteers/{self.volunteer_opportunity.opportunity_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_accepted_volunteer_opportunity_for_volunteer(self):
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_volunteer_token)
        response = self.rest_client.get(
            f"/api/opportunity/volunteer/accepted/{self.volunteer_opportunity.volunteer_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_volunteer_opportunity_by_id(self):
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_volunteer_token)
        response = self.rest_client.get(
            f"/api/opportunity/getVolOpp/{self.volunteer_opportunity.id}")
        self.assertEqual(response.status_code, 200)

    def test_complete_opportunity(self):
        data = {
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

        opportunity_approved = Opportunity.objects.create(**data)
        opportunity_approved.state = OpportunityState.APPROVED
        opportunity_approved.save()
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_vio_token)
        response = self.rest_client.post(
            f"/api/opportunity/completeOpportunity/{opportunity_approved.id}")
        self.assertEqual(response.status_code, 200)

    """
        def test_register_opportunity(self):
        self.rest_client.credentials(HTTP_AUTHORIZATION="Bearer " + self.main_vio_token)
        data = {
            "name": "Shramadhana at Sinharaja.",
            "description": "Shramadhana at sinharaja forest resovior",
            "address": "address to gether together",
            "district": "district of the Shramadhana",
            "start_date": "2021-10-25",
            "end_date": "2021-10-30",
            "goals": "The sharamadhana is organized to make the sharamadhana to protect earth",
            "contactPersonNumber": "0776685899",
            "numVolunteers": 3
        }

        response = self.rest_client.post("/api/opportunity/register", data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], data["name"])
    
    """
