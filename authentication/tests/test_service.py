from rest_framework.test import APITestCase

from authentication.enums import UserType
from authentication.models import User
from authentication.services import AuthService
from helpers.token_generators import gen_email_token


class TestAuthenticationService(APITestCase):
    def test_verify_email(self):
        user = User.objects.create_user('devin.18@cse.mrt.ac.lk', UserType.VOLUNTEER, 'password', gen_email_token())
        self.assertTrue(AuthService.verify_email(user.email_token))
        self.assertFalse(AuthService.verify_email(user.email_token))
