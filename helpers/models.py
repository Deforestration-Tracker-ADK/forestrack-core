from django.db import models

from authentication.enums import UserType


def get_profile_user(user):
    if user.user_type == UserType.VOLUNTEER:
        return user.volunteer

    if user.user_type == UserType.VIO:
        return user.vio


class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)
