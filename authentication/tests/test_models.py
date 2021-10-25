from rest_framework.test import APITestCase

from authentication.models import User, UserType
from helpers.token_generators import gen_email_token


class TestUserModel(APITestCase):

    def test_create_user(self):
        user = User.objects.create_user('devin.18@cse.mrt.ac.lk', UserType.VOLUNTEER, 'password', gen_email_token())
        self.assertIsInstance(user, User)
        self.assertFalse(user.is_staff)
        self.assertEqual("devin.18@cse.mrt.ac.lk", user.email)
        user.delete()

    def test_create_super_user(self):
        user = User.objects.create_superuser("donthackmeplease1710@gmail.com", UserType.VOLUNTEER, "super_password",
                                             gen_email_token())
        self.assertIsInstance(user, User)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual("donthackmeplease1710@gmail.com", user.email)
        user.delete()

    def test_raises_error_when_no_email_is_supplied(self):
        self.assertRaises(ValueError, User.objects.create_user, email='', user_type=UserType.VOLUNTEER,
                          password='password', email_token=gen_email_token())

    def test_raises_error_when_super_user_is_not_staff(self):
        self.assertRaises(ValueError, User.objects.create_superuser, email='', user_type=UserType.VOLUNTEER,
                          password='password', email_token=gen_email_token(), is_staff=False)

    def test_raises_error_when_super_user_is_not_staff(self):
        self.assertRaises(ValueError, User.objects.create_superuser, email='', user_type=UserType.VOLUNTEER,
                          password='password', email_token=gen_email_token(), is_superuser=False)
