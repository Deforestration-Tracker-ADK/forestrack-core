from rest_framework.test import APITestCase

from authentication.enums import UserType
from authentication.models import User
from helpers.token_generators import gen_email_token
from vio.models import Vio


class TestVioModel(APITestCase):
    def setUp(self) -> None:
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

    def test_create_vio(self):
        user_details = {
            **self.main_vio_data["user"],
            "user_type": UserType.VIO,
            "email_token": gen_email_token(),
        }
        user = User.objects.create(**user_details)

        vio_details = {**self.main_vio_data, "user": user}

        vio = Vio.objects.create(**vio_details)

        self.assertEqual(vio.registrationNo, self.main_vio_data["registrationNo"])
        self.assertEqual(vio.name, self.main_vio_data["name"])
        vio.delete()
        user.delete()
