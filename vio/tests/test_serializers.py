from rest_framework.test import APITestCase

from authentication.enums import UserType
from authentication.models import User
from helpers.token_generators import gen_email_token
from vio.models import Vio
from vio.serializers import VioRegisterSerializer


class TestVioSerializer(APITestCase):
    def setUp(self) -> None:
        self.serializer_class = VioRegisterSerializer
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

    def test_serializer_validation_accept(self):
        serializer = self.serializer_class(data=self.main_vio_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_validation_registration_date_in_future(self):
        data = {
            **self.main_vio_data,
            "registrationDate": "2098-04-05"
        }

        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_validation_contact_number_in_future(self):
        data = {
            **self.main_vio_data,
            "contactNumber": "0778489387854"
        }

        serializer = self.serializer_class(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_validation_nic_already_exist(self):
        user_details = {
            **self.main_vio_data["user"],
            "user_type": UserType.VIO,
            "email_token": gen_email_token(),
        }
        user = User.objects.create(**user_details)

        vio_details = {**self.main_vio_data, "user": user}

        vio = Vio.objects.create(**vio_details)
        serializer = self.serializer_class(data=self.main_vio_data)
        self.assertFalse(serializer.is_valid())
        vio.delete()

    def test_serializer_create(self):
        serializer = self.serializer_class(data=self.main_vio_data)
        self.assertTrue(serializer.is_valid())
        vio = serializer.save()
        self.assertEqual(vio.description, self.main_vio_data["description"])
        self.assertEqual(vio.name, self.main_vio_data["name"])
