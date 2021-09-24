from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication.enums import VolunteerVioState
from authentication.models import User
from helpers.models import TrackingModel


class GenderType(models.TextChoices):
    MALE = 'MALE', _('Male')
    FEMALE = 'FEMALE', _('Female')
    UNSPECIFIED = 'UNSPECIFIED', _('Unspecified')


class LanguageType(models.TextChoices):
    SINHALA = 'SINHALA', _('Sinhala')
    ENGLISH = 'ENGLISH', _('English')
    TAMIL = 'TAMIL', _('Tamil')


class HighestEducation(models.TextChoices):
    OL = 'OL', _('OL')
    AL = 'AL', _('AL')
    UNDERGRADUATE = 'UNDERGRADUATE', _('Undergraduate')
    POSTGRADUATE = 'POSTGRADUATE', _('Postgraduate')


# Create your models here.
class Volunteer(TrackingModel):
    """
    Database model that describes a volunteer in the system
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100, help_text="First name of the volunteer", blank=False)
    last_name = models.CharField(max_length=100, help_text="Last name of the Volunteer", blank=False)
    nic = models.CharField(max_length=15, help_text="NIC number of the volunteer", blank=False, unique=True)
    nameNIC = models.CharField(max_length=100, help_text="Name as stated in the NIC", blank=True)
    gender = models.CharField(max_length=15, choices=GenderType.choices, blank=True,
                              help_text="gender of the volunteer")
    district = models.CharField(max_length=100, help_text="District of the volunteer residence", blank=True)
    address = models.CharField(max_length=100, help_text="Volunteers address of residence", blank=True)
    imageUrl = models.CharField(max_length=100, help_text="Volunteers image url", blank=True)
    specialConditions = models.CharField(max_length=250, help_text="Any special conditions of the user", blank=True)
    preferredLanguage = models.CharField(max_length=100, choices=LanguageType.choices, default=LanguageType.SINHALA,
                                         help_text="Preferred Language of the volunteer", blank=True)
    highestEducation = models.CharField(max_length=100, choices=HighestEducation.choices,
                                        help_text="Highest Education of the volunteer", blank=True)

    state = models.CharField(
        max_length=25,
        blank=False,
        choices=VolunteerVioState.choices,
        default=VolunteerVioState.UNAPPROVED)
