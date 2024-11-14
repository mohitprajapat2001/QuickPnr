# Signals to Send PNR Details When PNR Instance Created
from django.db.models.signals import post_save
from django.dispatch import receiver

# from pnr.tasks import send_pnr_details
from pnr.models import PnrDetail


@receiver(post_save, sender=PnrDetail)
def send_pnr_details_signal(sender, instance, created, **kwargs):
    # TODO Update PNR Details Model Such That Takes User M2M Who Requested for PNR Details
    return True
    # if created:
    # send_pnr_details.delay(instance.user_id, instance.id)
