import os

import environ
from django.db import transaction
from dotenv import load_dotenv

from admin.models import SystemAdmin
from authentication.enums import UserType
from authentication.models import User
from helpers.email_sender.admin_invitation import admin_invitation_email
from helpers.token_generators import gen_password, gen_email_token

load_dotenv()
env = environ.Env()
frontend_host = os.environ.get('FRONTEND_HOST') if not os.environ.get(
    'FRONTEND_HOST') is None else "http://localhost:3000"


def create_core_admin():
    core_admin_email = env("CORE_ADMIN_EMAIL")
    core_admin_password = env("CORE_ADMIN_PASSWORD", default=None)
    core_admin_first_name = env("CORE_ADMIN_FIRST_NAME", default="Devin")
    core_admin_last_name = env("CORE_ADMIN_LAST_NAME", default="De Silva")
    core_admin_nic = env("CORE_ADMIN_NIC", default="982910110V")

    if core_admin_email is None:
        raise Exception("Core admin email not available please provide core admin email.")

    if User.objects.filter(email=core_admin_email).exists():
        return User.objects.get(email=core_admin_email)

    return create_admin(core_admin_email, core_admin_first_name, core_admin_last_name, core_admin_nic,
                        core_admin_password)


@transaction.atomic()
def create_admin(email, first_name, last_name, nic, password=None):
    if not password:
        password = gen_password()
    email_token = gen_email_token()
    email_details = {
        "email": email,
        "password": password,
        "token": email_token,
        "email_verify_link": f"{frontend_host}/VerifyEmail/{email_token}"
    }
    admin_invitation_email(email, email_details)
    user = User.objects.create_superuser(email, UserType.ADMIN, password, email_token)
    admin = SystemAdmin.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        nic=nic,
    )
    return SystemAdmin.objects.filter(user=user).values()[0]
