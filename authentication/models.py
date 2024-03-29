from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from authentication.enums import UserType, UserState
from helpers.models import TrackingModel


class ForestRackUserManager(UserManager):
    def _create_user(self, email, user_type, password, email_token, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.user_type = user_type
        user.email_token = email_token
        user.save(using=self._db)
        return user

    def create_user(self, email, user_type, password, email_token, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, user_type, password, email_token, **extra_fields)

    def create_superuser(self, email, user_type, password, email_token, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, user_type, password, email_token, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    """
        An abstract base class implementing a fully featured User model with
        admin-compliant permissions.

        Username and password are required. Other fields are optional.
    """

    email = models.EmailField(_('email address'), blank=False, unique=True)
    user_type = models.CharField(
        _("user_type"),
        max_length=50,
        choices=UserType.choices,
        blank=False,
        default=UserType.VOLUNTEER,
    )

    email_token = models.CharField(
        _("email_token"),
        max_length=100,
        blank=False,
        unique=True
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    state = models.CharField(
        max_length=25,
        blank=False,
        choices=UserState.choices,
        default=UserState.EMAIL_UNVERIFIED)

    objects = ForestRackUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def token(self):
        token = jwt.encode({
            'id': self.id,
            'email': self.email,
            'user_type': self.user_type,
            'state': self.state,
            'exp': datetime.utcnow() + timedelta(hours=24 * 30)

        },
            settings.SECRET_KEY,
            algorithm='HS256',
        )
        return token
