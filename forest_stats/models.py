from django.db import models

# Create your models here.
from helpers.models import TrackingModel


class ForestStats(TrackingModel):
    district = models.CharField(blank=False, max_length=100)
    water = models.DecimalField(blank=False, default=0, decimal_places=5, max_digits=15)
    artificial_bare_ground = models.DecimalField(blank=False, default=0, decimal_places=5, max_digits=15)
    artificial_natural_ground = models.DecimalField(blank=False, default=0, decimal_places=5, max_digits=15)
    woody = models.DecimalField(blank=False, default=0, decimal_places=5, max_digits=15)
    non_woody_cultivated = models.DecimalField(blank=False, default=0, decimal_places=5, max_digits=15)
    non_woody_natural = models.DecimalField(blank=False, default=0, decimal_places=5, max_digits=15)
    mean_ndvi = models.DecimalField(blank=False, default=0, decimal_places=5, max_digits=15)
    mean_burn_index = models.DecimalField(blank=False, default=0, decimal_places=5, max_digits=15)
