"""Utility Models Admin Panel"""

from django.contrib import admin
from utils.utils import get_model

EmailTemplate = get_model("quickpnr", "EmailTemplate")


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "email_type",
        "is_html",
        "status",
        "created",
        "modified",
    )
    list_filter = ("status", "email_type", "is_html")
    search_fields = ("subject", "body", "template")
    readonly_fields = ("created", "modified")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "subject",
                    "body",
                    "template",
                    "is_html",
                    "email_type",
                    "status",
                ),
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "created",
                    "modified",
                ),
            },
        ),
    )
