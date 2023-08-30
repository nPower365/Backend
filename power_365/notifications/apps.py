from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'power_365.notifications'
    verbose_name = _("Notifications")

    def ready(self):
        try:
            import power_365.notifications.signals  # noqa F401
        except ImportError:
            pass
