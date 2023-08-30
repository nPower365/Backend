from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from power_365.notifications.models import Notification
from power_365.notifications.tasks import send_notification
User = get_user_model()


@receiver(post_save, sender=Notification)
def send_user_notification(sender, instance, created, **kwargs):
    if created:
        send_notification.apply_async(
            (instance.id,), countdown=10)
