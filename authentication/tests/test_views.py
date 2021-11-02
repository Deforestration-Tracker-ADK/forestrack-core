from rest_framework.test import APITestCase, APIClient

from authentication.enums import UserType
from authentication.models import User
from authentication.views import get_profile_details
from helpers.token_generators import gen_email_token
from vio.models import Vio
from volunteer.models import Volunteer


class AuthIntegrationTests(APITestCase):
    def setUp(self) -> None:
        self.rest_client = APIClient()
        self.main_volunteer_user = User.objects.create_user('devin.18@cse.mrt.ac.lk', UserType.VOLUNTEER, 'password',
                                                            gen_email_token())

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
        self.vol_user = User.objects.create(**user_details)
        volunteer_details = {**self.main_volunteer_data, "user": self.vol_user}
        self.volunteer = Volunteer.objects.create(**volunteer_details)

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
        self.vio_user = User.objects.create(**user_details)
        vio_details = {**self.main_vio_data, "user": self.vio_user}
        self.vio = Vio.objects.create(**vio_details)

    def test_login_user_must_verify_email(self):
        data = {
            "email": 'devin.18@cse.mrt.ac.lk',
            "password": "password"
        }

        response = self.rest_client.post("/api/auth/login", data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'message': 'User must verify email'})

    def test_verify_email(self):
        response = self.rest_client.post(f"/api/auth/email_verify/{self.main_volunteer_user.email_token}")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)

    def test_verify_email_invalid_token(self):
        response = self.rest_client.post(f"/api/auth/email_verify/{gen_email_token()}")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"message": "Invalid email token"})

    def test_login(self):
        data = {
            "email": 'devin.18@cse.mrt.ac.lk',
            "password": "password"
        }
        self.rest_client.post(f"/api/auth/email_verify/{self.main_volunteer_user.email_token}")
        response = self.rest_client.post("/api/auth/login", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], self.main_volunteer_user.email)
        self.assertEqual(response.data["user_type"], self.main_volunteer_user.user_type)

    def test_login_invalid_credentials(self):
        data = {
            "email": 'devin.18@cse.mrt.ac.lk',
            "password": "not_password"
        }
        response = self.rest_client.post("/api/auth/login", data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"message": "Invalid credentials try again"})

    def test_get_profile_details(self):
        volunteer = get_profile_details(self.vol_user)
        self.assertEqual(volunteer.nic, self.volunteer.nic)

        vio = get_profile_details(self.vio_user)
        self.assertEqual(vio.registrationNo, self.vio.registrationNo)

    def tearDown(self) -> None:
        self.main_volunteer_user.delete()
