"""Quick PNR Basic Utilities Models"""

from django.db import models
from django_extensions.db.models import ActivatorModel, TimeStampedModel
from django.utils.translation import gettext_lazy as _
from utils.constants import EmailTemplates


class EmailTemplate(TimeStampedModel, ActivatorModel):
    """model for storing email templates"""

    subject = models.CharField(max_length=255, verbose_name=_("subject"))
    body = models.TextField(verbose_name=_("body"))
    template = models.TextField(null=True, blank=True)
    is_html = models.BooleanField(null=True, blank=True)
    email_type = models.CharField(
        max_length=50, choices=EmailTemplates.EMAIL_TYPES, null=True, blank=True
    )

    def __str__(self) -> str:
        """
        Returns a string representation of the model.
        Returns:
            str: The subject of the email template.
        """
        return self.subject
