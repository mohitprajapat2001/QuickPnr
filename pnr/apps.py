from django.apps import AppConfig


class PnrConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pnr"

    # PNR App - Signal
    def ready(self):
        import pnr.signals  # noqa: F401
