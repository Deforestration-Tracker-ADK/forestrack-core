from django.db import models
from django.utils.translation import gettext_lazy as _


class OpportunityState(models.TextChoices):
    DELETED = 'DELETE', _('Deleted')
    UNAPPROVED = 'UNAPPROVED', _('Unapproved')
    REJECTED = "REJECTED", _('Rejected')
    APPROVED = 'APPROVED', _('Approved')
    COMPLETED = "COMPLETED", _("Complete")


class VolunteerOpportunityState(models.TextChoices):
    ACCEPTED = 'ACCEPTED', _('Accepted')
    REJECTED = 'REJECTED', _('Rejected')
    PENDING = 'PENDING', _('Pending')
    COMPLETED = "COMPLETED", _("Complete")
