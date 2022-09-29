import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.authentication.managers import UserManager
from apps.common.models import TimeStampedModel


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """
    Description: database table used for user
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_('first name'), max_length=50, blank=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True)
    username = models.CharField(_('username'), max_length=50, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    email_verification_token = models.CharField(
        _('email verification token'), max_length=256, blank=True
    )
    email_verification_otp = models.CharField(
        _('email verification token'), max_length=256, blank=True
    )
    password_otp = models.CharField(_('password token'), max_length=256, blank=True)
    password_hashcode = models.CharField(_('password hashcode'), max_length=256, blank=True)
    email_verified = models.BooleanField(_('email verification status'), default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def logout(self):
        """
        used to logout the user
        """
        self.oauth2_provider_accesstoken.all().delete()


    class Meta:
        """
        Meta class
        """
        db_table = "auth_users"
