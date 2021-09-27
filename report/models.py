from django.db import models

# Create your models here.
from helpers.models import TrackingModel


class DeforestationReports(TrackingModel):
    long = models.DecimalField(blank=False, decimal_places=3, max_digits=10)
    lat = models.DecimalField(blank=False, decimal_places=3, max_digits=10)
