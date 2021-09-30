import uuid

from django.utils.crypto import get_random_string


def gen_email_token():
    return uuid.uuid4()


def gen_password(password_size=10):
    return get_random_string(length=password_size)
