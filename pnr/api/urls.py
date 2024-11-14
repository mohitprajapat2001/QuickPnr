# PNR Scrapping URL

from django.urls import path
from pnr.api.api import PnrScrapper

urlpatterns = [
    path("fetch/", PnrScrapper.as_view()),
]
