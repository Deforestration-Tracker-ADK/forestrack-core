from django.db import models

from authentication.enums import VolunteerVioState
from authentication.models import User
from helpers.models import TrackingModel


# Create your models here.
class Vio(TrackingModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100, help_text="name of the Vio", blank=False)
    description = models.CharField(max_length=255, help_text="Description of the Vio", blank=False)
    imageUrl = models.CharField(max_length=100, help_text="VIO image url", blank=True)
    registrationNo = models.CharField(max_length=100, help_text="Registration Number of the Vio", blank=True)
    address = models.CharField(max_length=250, help_text="Register address of the vio", blank=True)
    district = models.CharField(max_length=100, help_text="District of the vio residence", blank=True)
    contactNumber = models.CharField(max_length=15, help_text="Contact number of volunteer", blank=False)
    registrationDate = models.DateField(blank=False)
    state = models.CharField(
        max_length=25,
        blank=False,
        choices=VolunteerVioState.choices,
        default=VolunteerVioState.UNAPPROVED)
