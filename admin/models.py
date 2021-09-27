from django.db import models

# Create your models here.
from authentication.models import User
from helpers.models import TrackingModel


class Admin(TrackingModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100, help_text="First name of the volunteer", blank=False)
    last_name = models.CharField(max_length=100, help_text="Last name of the Volunteer", blank=False)
    nic = models.CharField(max_length=15, help_text="NIC number of the volunteer", blank=False, unique=True)
