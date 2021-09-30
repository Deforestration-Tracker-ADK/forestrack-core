from cloudinary.models import CloudinaryField
from django.db import models

# Create your models here.
from helpers.models import TrackingModel
from volunteer.models import Volunteer


class DeforestationReport(TrackingModel):
    long = models.DecimalField(blank=True, decimal_places=7, max_digits=10)
    lat = models.DecimalField(blank=True, decimal_places=7, max_digits=10)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    district = models.CharField(blank=True, max_length=25)
    severity = models.IntegerField(blank=True)
    recent = models.BooleanField(blank=True)
    action_description = models.CharField(blank=True, max_length=500)
    special_notes = models.CharField(blank=True, max_length=500)


class ReportPhoto(TrackingModel):
    report = models.ForeignKey(DeforestationReport, on_delete=models.CASCADE, )
    image = CloudinaryField('image')
