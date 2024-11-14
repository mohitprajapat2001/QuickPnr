# Register your models here.
from pnr.models import PassengerDetail, PnrDetail
from django.contrib import admin


# @admin.register(PnrVersion)
# class PnrVersionAdmin(admin.ModelAdmin):
#     list_display = ("pnr_details", "version")
#     list_filter = ("pnr_details", "version")
#     search_fields = ("pnr_details", "version")


@admin.register(PassengerDetail)
class PassengerDetailAdmin(admin.ModelAdmin):
    list_display = ("name", "pnr_details", "booking_status", "current_status")
    list_filter = ("booking_status", "current_status")
    search_fields = ("name", "pnr_details")


@admin.register(PnrDetail)
class PnrDetailAdmin(admin.ModelAdmin):
    list_display = ("pnr", "train_number", "train_name", "boarding_date", "status")
    list_filter = ("status", "boarding_date")
    search_fields = ("pnr", "train_number", "train_name")
    readonly_fields = ("created", "modified")
