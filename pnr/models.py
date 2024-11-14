# Pnr Scrapping Details Model
from django.db import models
from pnr.constants import ModelsConstants, ModelVerbose
from django_extensions.db.models import ActivatorModel, TimeStampedModel


class PnrDetail(ActivatorModel, TimeStampedModel):
    """Store PNR Details"""

    pnr = models.BigIntegerField(verbose_name=ModelVerbose.PNR_NUMBER)
    train_number = models.CharField(
        verbose_name=ModelVerbose.TRAIN_NUMBER, max_length=8
    )
    train_name = models.CharField(max_length=132, verbose_name=ModelVerbose.TRAIN_NAME)
    boarding_date = models.DateTimeField(verbose_name=ModelVerbose.BOARDING_DATE)
    boarding_point = models.CharField(
        max_length=8, verbose_name=ModelVerbose.BOARDING_POINT, null=True, blank=True
    )
    reserved_from = models.CharField(verbose_name=ModelVerbose.RESERVED_FROM)
    reserved_to = models.CharField(max_length=8, verbose_name=ModelVerbose.RESERVED_TO)
    reserved_class = models.CharField(
        max_length=8, verbose_name=ModelVerbose.RESERVED_CLASS
    )
    fare = models.DecimalField(
        decimal_places=2, max_digits=10, verbose_name=ModelVerbose.FARE
    )
    remark = models.CharField(
        max_length=64, verbose_name=ModelVerbose.REMARK, null=True, blank=True
    )
    train_status = models.CharField(
        max_length=64, verbose_name=ModelVerbose.TRAIN_STATUS, null=True, blank=True
    )
    charting_status = models.CharField(
        max_length=64, verbose_name=ModelVerbose.CHARTING_STATUS
    )
    expiry = models.DateTimeField(verbose_name=ModelVerbose.EXPIRY)
    users = models.ManyToManyField("users.User", blank=True, related_name="pnrs")

    class Meta:
        verbose_name = ModelVerbose.PNR_DETAIL

    def soft_delete(self):
        """Soft Delete PNR Details"""
        self.status = ActivatorModel.INACTIVE_STATUS
        self.save(update_fields=["status"])

    def __str__(self):
        return str(self.pnr)


class PassengerDetail(models.Model):
    """Store Passenger Details"""

    pnr_details = models.ForeignKey(
        "pnr.PnrDetail",
        on_delete=models.CASCADE,
        related_name=ModelsConstants.PASSENGERS_DETAILS,
    )
    name = models.CharField(max_length=64, verbose_name=ModelVerbose.NAME)
    booking_status = models.CharField(
        max_length=64, verbose_name=ModelVerbose.BOOKING_STATUS
    )
    current_status = models.CharField(
        max_length=64, verbose_name=ModelVerbose.CURRENT_STATUS
    )
    coach_position = models.CharField(
        max_length=64, verbose_name=ModelVerbose.COACH_POSITION, null=True, blank=True
    )

    class Meta:
        verbose_name = ModelVerbose.PASSENGER_DETAIL
