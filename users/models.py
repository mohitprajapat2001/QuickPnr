from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy
from users.constants import (
    ModelFields,
    THUMBNAIL_PREVIEW_TAG,
    THUMBNAIL_PREVIEW_HTML,
)
from django.utils.html import format_html
from django_extensions.db.models import TimeStampedModel
from users.constants import VerboseNames


def _upload_to(self, filename):
    """Upload User Profile Image"""
    return "users/{id}/{filename}".format(id=self.id, filename=filename)


def _random_otp(self):
    import random

    return random.randint(100000, 999999)


class User(AbstractUser):
    """Abstract User Model"""

    image = models.ImageField(
        verbose_name=VerboseNames.PROFILE_IMAGE,
        upload_to=_upload_to,
        blank=True,
        null=True,
    )
    email = models.EmailField(verbose_name=VerboseNames.EMAIL_ADDRESS, unique=True)
    is_verified = models.IntegerField(
        verbose_name=VerboseNames.VERIFICATION_STATUS,
        choices=ModelFields.STATUS_CHOICES,
        default=ModelFields.INACTIVE_STATUS,
    )
    age = models.IntegerField(verbose_name=VerboseNames.AGE, blank=True, null=True)
    address = models.TextField(verbose_name=VerboseNames.ADDRESS, blank=True, null=True)
    google_id = models.CharField(
        blank=True,
        null=True,
        verbose_name=VerboseNames.GOOGLE_ID,
        unique=True,
        max_length=255,
    )

    @property
    def profile_image(self):
        """Profile Image Viewer"""
        if self.image:
            return format_html(THUMBNAIL_PREVIEW_TAG.format(img=self.image.url))
        return format_html(THUMBNAIL_PREVIEW_HTML)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse_lazy("user:details", kwargs={"username": self.username})


class Otp(TimeStampedModel):
    """OTP Models to Store OTP Details"""

    otp = models.IntegerField(default=_random_otp)
    expiry = models.DateTimeField()
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="otp"
    )

    def __str__(self):
        return "{user}'s OTP".format(user=self.user.username)

    def save(self, *args, **kwargs):
        return super(Otp, self).save(*args, **kwargs)
