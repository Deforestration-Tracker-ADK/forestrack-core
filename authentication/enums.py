import enum

from django.db import models
from django.utils.translation import gettext_lazy as _


class VioTypes(enum.Enum):
    STATE_INSTITUTE = 'STATE_INSTITUTE',
    STATE_ACADEMIA = 'STATE_ACADEMIA',
    PRIVATE_ORGANIZATION = 'PRIVATE_ORGANIZATION',
    PRIVATE_ACADEMIA = 'PRIVATE_ACADEMIA',
    NONPROFIT = 'NONPROFIT',
    SCHOOL = 'SCHOOL',


class UserType(models.TextChoices):
    VOLUNTEER = 'VOL', _('Volunteer')
    VIO = 'VIO', _('Vio')
    ADMIN = 'AD', _('Admin')


class VolunteerVioState(models.TextChoices):
    DELETED = 'DELETE', _('Deleted')
    UNAPPROVED = 'UNAPPROVED', _('Unapproved')
    REJECTED = 'REJECTED', _('Rejected')
    APPROVED = 'APPROVED', _('Approved')


class UserState(models.TextChoices):
    EMAIL_UNVERIFIED = "EMAIL_UNVERIFIED", _("Email_Unverified")
    DELETED = 'DELETE', _('Deleted')
    EMAIL_VERIFIED = 'EMAIL_VERIFIED', _('Email_Verified')
