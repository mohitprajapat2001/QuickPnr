from django.contrib import admin
from utils.utils import get_model
from django.contrib.auth.admin import UserAdmin

User = get_model("users", "User")
Otp = get_model("users", "Otp")

admin.site.register(Otp)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "age",
        "address",
    )
    readonly_fields = ("id", "last_login", "date_joined", "profile_image", "google_id")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    fieldsets = (
        (
            None,
            {
                "fields": ["id", "google_id"],
            },
        ),
        (
            "Personal Details",
            {
                "fields": ("username", "email", "password", "first_name", "last_name"),
            },
        ),
        (
            "User Details",
            {
                "fields": ("age", "address"),
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
        ("Groups", {"fields": ("groups", "user_permissions")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_verified", "is_superuser")},
        ),
        (
            "Profile Image",
            {"fields": ("profile_image", "image")},
        ),
    )
    filter_horizontal = ("groups", "user_permissions")
