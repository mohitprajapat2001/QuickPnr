from dotenv import dotenv_values
from django.utils.translation import gettext_noop as _
from os import path, getcwd

env = dotenv_values(".env")


# Settings Constants
# =====================================================
class Settings:
    """Settings Constants"""

    SECRET_KEY = env.get("SECRET_KEY")
    ROOT_URLCONF = "quickpnr.urls"
    AUTH_USER_MODEL = "users.User"
    WSGI_APPLICATION = "quickpnr.wsgi.application"
    DJANGO_DATABASE_URL = env.get("DJANGO_DATABASE_URL")
    LANGUAGE_CODE = "en-us"
    TIME_ZONE = "Asia/Kolkata"
    USE_I18N = True
    USE_TZ = True
    STATIC_URL = "static/"
    STATIC_ROOT = "assets/"
    STATIC_FILES_DIRS = "templates/static/"
    TEMPLATES_URLS = "templates/"
    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
    REDIS_URL = env.get("REDIS_URL")
    MEDIA_URL = "media/"
    MEDIA_ROOT = "media/"


# Email Configurations
# =====================================================
class EmailConfig:
    """Email Configurations"""

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    PORT_465 = 465
    PORT_587 = 587
    EMAIL_HOST_USER = env.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env.get("EMAIL_HOST_PASSWORD")


# Celery Configuration
# =====================================================
class CeleryConfig:
    """Celery Configuration"""

    CELERY_BROKER_URL = "redis://localhost:6379/0"


# Urls Namespaces & Reverse
# =====================================================
class Urls:
    """Urls Namespace & Reverses"""


# Email Templates
# ============================BASE_DIR=========================
class EmailTemplates:
    """Email Templates"""

    VERIFY_EMAIL = "verify_email"
    REGISTRED_SUCCESSFULLY = "registered"
    PNR_DETAILS = "pnr_details"
    PASSWORD_RESET = "password_reset"
    PASSWORD_RESET_DONE = "password_reset_done"

    EMAIL_TYPES = (
        (VERIFY_EMAIL, _("Verify Email")),
        (REGISTRED_SUCCESSFULLY, _("Registered Successfully")),
        (PNR_DETAILS, _("PNR Details")),
        (PASSWORD_RESET_DONE, _("Password Reset Done")),
        (PASSWORD_RESET, _("Password Reset")),
    )


# PNR Utility Constants
# =====================================================
class PnrConstants:
    """PNR Utility Constants"""

    SCRAPPING_URL = "https://www.indianrail.gov.in/enquiry/PNR/PnrEnquiry.html"


# Elements IDs
# =====================================================
class IDs:
    """Scrapping Element IDs"""

    PNR_INPUT = "inputPnrNo"
    CAPTCHA_MODAL = "modal1"
    CAPTCHA_IMAGE = "CaptchaImgID"
    CAPTCHA_SUBMIT = "submitPnrNo"
    INPUT_CACHE = "inputCaptcha"


# Elements & Their Types
# =====================================================
class ElementTypes:
    """Scrapping Element Types"""

    INPUT = "input"
    BUTTON = "button"
    IMAGE = "img"
    SRC = "src"
    TEXT = "text"
    TYPE = "type"
    NUMBER = "number"
    SUBMIT = "submit"
    CAPTCHA_IMAGE_TEMPORARY = path.join(getcwd(), ".images/captcha.png")
    PAGE_SS = path.join(getcwd(), ".images/page.png")
