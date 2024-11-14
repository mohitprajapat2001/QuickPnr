"""Custom Exceptions Cases for PNR Scrapping"""

from rest_framework.serializers import ValidationError


class PNRNotFound(BaseException):
    """PNR Not Found Base Exceptions"""

    pass


class InvalidPnrNumber(ValidationError):
    """Invalid PNR Number Exception"""

    pass
