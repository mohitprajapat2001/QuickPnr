# PNR Scrapping Constants


class ModelVerbose:
    """Model Verbose Names"""

    PNR_NUMBER = "pnr number"
    TRAIN_NUMBER = "train number"
    TRAIN_NAME = "train name"
    BOARDING_DATE = "boarding date"
    BOARDING_POINT = "boarding point"
    RESERVED_FROM = "reserved from"
    RESERVED_TO = "reserved to"
    RESERVED_CLASS = "reserved class"
    FARE = "fare"
    REMARK = "remark"
    TRAIN_STATUS = "train status"
    NAME = "name"
    CHARTING_STATUS = "charting status"
    BOOKING_STATUS = "booking status"
    CURRENT_STATUS = "current status"
    EXPIRY = "pnr expiry"
    COACH_POSITION = "coach position"
    PNR_DETAIL = "PNR Detail"
    PASSENGER_DETAIL = "Passenger Detail"


class ModelsConstants:
    """Models Constants"""

    PASSENGERS_DETAILS = "passengers_details"


class ReponseMessages:
    """Message Constants"""

    MULTIPLE_PNR_FOUND_ERROR_HANDLED = "Multiple PNRs Found Error Handled, Last Modified PNR Saved Else Deleted - {pnr}"
    MULTIPLE_PNR_FOUND = "Multiple PNR Found"
    PNR_NOT_FOUND = "PNR Not Found"
    PNR_DETAILS_MAILED = "PNR Details Mailed Successfully"
    FLUSHED_PNR = "Flushed PNR Requested"


class ScrappingConstants:
    """PNR Scrapping Constants"""

    PNR_NUMBER_ENTERED = "PNR Number Entered Successfully"
    CAPTCHA_MODEL_OPENED = "Captcha Modal Opened"
    INVALID_PAGE = "Invalid Page"


class PnrSerializerConstants:
    """PNR Serializers Constants"""

    INVALID_PNR = "Invalid PNR Number"
