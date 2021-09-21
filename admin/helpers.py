import environ
from django.db import transaction
from dotenv import load_dotenv

from authentication.enums import UserType
from authentication.models import User
from helpers.email_sender.admin_invitation import admin_invitation_email
from helpers.token_generators import gen_password, gen_email_token

load_dotenv()
env = environ.Env()


def create_core_admin():
    core_admin_email = env("CORE_ADMIN_EMAIL")
    core_admin_password = env("CORE_ADMIN_PASSWORD", default=None)
    if core_admin_email is None:
        raise Exception("Core admin email not available please provide core admin email.")

    if User.objects.filter(email=core_admin_email).exists():
        return User.objects.get(email=core_admin_email)

    return create_admin(core_admin_email, core_admin_password)


@transaction.atomic()
def create_admin(email, password=None):
    if not password:
        password = gen_password()
    email_token = gen_email_token()
    email_details = {
        "email": email,
        "password": password,
        "token": email_token,
    }
    admin_invitation_email(email, email_details)
    return User.objects.create_superuser(email, UserType.ADMIN, password, email_token)
