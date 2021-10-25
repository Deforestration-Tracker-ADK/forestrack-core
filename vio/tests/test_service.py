from rest_framework.test import APITestCase

from authentication.enums import VolunteerVioState
from vio.serializers import VioRegisterSerializer
from vio.services import VioService


class TestVioService(APITestCase):
    def setUp(self) -> None:
        self.serializer_class = VioRegisterSerializer
        self.service = VioService
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

        vio1_serializer = self.serializer_class(data=self.main_vio_data)
        self.assertTrue(vio1_serializer.is_valid())
        self.vio1 = vio1_serializer.save()

        vio2_data = {
            **self.main_vio_data,
            "registrationNo": "982970767v",
            "user": {
                "email": "vio2@gmail.com",
                "password": "password"
            }
        }

        vio2_serializer = self.serializer_class(data=vio2_data)
        self.assertTrue(vio2_serializer.is_valid())
        self.vio2 = vio2_serializer.save()

        vol3_data = {
            **self.main_vio_data,
            "registrationNo": "982767767v",
            "user": {
                "email": "vio3@gmail.com",
                "password": "password"
            }
        }

        vio3_serializer = self.serializer_class(data=vol3_data)
        self.assertTrue(vio3_serializer.is_valid())
        self.vio3 = vio3_serializer.save()

    def test_getVio(self):
        vio = self.service.getVio(state=VolunteerVioState.UNAPPROVED)
        self.assertEqual(len(vio), 3)
        self.assertEqual(vio[0]["description"], self.main_vio_data["description"])

        vio = self.service.getVio(state=VolunteerVioState.UNAPPROVED, num_of=2)
        self.assertEqual(len(vio), 2)
        self.assertEqual(vio[0]["description"], self.main_vio_data["description"])

    def test_getVioById(self):
        vio = self.service.getVioById(self.vio2.user_id)
        self.assertEqual("Ocean willl look amazing in the future and we will be apart of it", vio["description"])

        vio = self.service.getVioById(self.vio1.user_id)
        self.assertEqual("vio1@gmail.com", vio["user"]["email"])
