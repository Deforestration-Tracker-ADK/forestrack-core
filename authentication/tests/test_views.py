from rest_framework.test import APITestCase, APIClient

from authentication.enums import UserType
from authentication.models import User
from helpers.token_generators import gen_email_token


class AuthIntegrationTests(APITestCase):
    def setUp(self) -> None:
        self.rest_client = APIClient()
        self.main_volunteer_user = User.objects.create_user('devin.18@cse.mrt.ac.lk', UserType.VOLUNTEER, 'password',
                                                            gen_email_token())

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

    def tearDown(self) -> None:
        self.main_volunteer_user.delete()
