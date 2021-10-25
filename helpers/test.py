import uuid

from rest_framework.test import APITestCase

from helpers.token_generators import gen_email_token, gen_password


class TokenGeneratorTestCase(APITestCase):
    def test_generate_email_token(self):
        email_token = gen_email_token()
        self.assertIsInstance(email_token, uuid.UUID)

    def test_generate_password(self):
        generated_password = gen_password()
        self.assertEqual(len(generated_password), 10)
