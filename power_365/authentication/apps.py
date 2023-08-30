from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthenticationConfig(AppConfig):
    name = "power_365.authentication"
    verbose_name = _("Authentication")

    def ready(self):
        try:
            import power_365.authentication.signals  # noqa F401
        except ImportError:
            pass
