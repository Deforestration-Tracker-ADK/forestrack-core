from django.db import models

# Create your models here.
from helpers.models import TrackingModel
from opportunity.enums import OpportunityState, VolunteerOpportunityState
from vio.models import Vio
from volunteer.models import Volunteer


class Opportunity(TrackingModel):
    vio = models.OneToOneField(Vio, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100, help_text="name of the Opportunity", blank=False)
    description = models.CharField(max_length=255, help_text="Description of the Opportunity", blank=False)
    address = models.CharField(max_length=250, help_text="Register address of the Opportunity", blank=True)
    district = models.CharField(max_length=100, help_text="District of the Opportunity residence", blank=True)
    state = models.CharField(
        max_length=25,
        blank=False,
        choices=OpportunityState.choices,
        default=OpportunityState.UNAPPROVED)


class VolunteerOpportunity(TrackingModel):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=25,
        blank=False,
        choices=VolunteerOpportunityState.choices,
        default=VolunteerOpportunityState.PENDING
    )
