from rest_framework.test import APITestCase

from authentication.enums import UserType
from authentication.models import User
from authentication.serializers import UserRegisterSerializer, email_choose
from helpers.token_generators import gen_email_token


class TestUserSerializer(APITestCase):
    """
    User serializer Testing Class
    """
    serializer_class = UserRegisterSerializer

    def test_serializer_validation_accept(self):
        """
        Test the validation passing scenario
        :return: None
        """

        data = {
            "email": "devin.17@cse.mrt.ac.lk",
            "password": "cartoonnetwork",
        }

        serializer = self.serializer_class(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_validation_raise_error(self):
        """
        Testing the serializer validation when a user with same email exist
        :return:
        """
        user = User.objects.create_user('devin.18@cse.mrt.ac.lk', UserType.VOLUNTEER, 'password', gen_email_token())
        data = {
            "email": "devin.18@cse.mrt.ac.lk",
            "password": "cartoonnetwork",
        }
        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())
        user.delete()

    def test_serializer_create_user(self):
        """
        Testing the serializer Create
        :return:
        """
        data = {
            "email": "devin.16@cse.mrt.ac.lk",
            "password": "cartoonnetwork",
        }
        serializer = self.serializer_class(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.create(data, UserType.VOLUNTEER)
        self.assertTrue(User.objects.filter(email=data["email"]).exists())

    def test_email_choose(self):
        """
        Testing email sending functionality
        :return:
        """
        data = {
            "email": "devin.18@cse.mrt.ac.lk",
            "email_verify_link": f"/VerifyEmail/937273283njqscaj"
        }

        email_choose(UserType.VOLUNTEER, data)
        email_choose(UserType.VIO, data)

        self.assertRaises(NotImplementedError, email_choose, user_type=UserType.ADMIN,
                          data=data)
