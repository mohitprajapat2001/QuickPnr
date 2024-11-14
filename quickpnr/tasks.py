"""Flush Expired PNR Details"""

from celery import shared_task
from utils.utils import get_model
from django.utils.timezone import now

PnrDetail = get_model("pnr", "PnrDetail")


@shared_task
def flush_pnr():
    """Flush Expired PNR Details"""
    pnrs = PnrDetail.objects.filter(expiry__lt=now())
    [pnr.soft_delete() for pnr in pnrs]
    return "PNR Details Flushed"
