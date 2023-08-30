from fcm_django.models import FCMDevice
from power_365.notifications.models import Notification
from firebase_admin.messaging import Message, Notification as FCMNotification
from django.contrib.auth import get_user_model
from config import celery_app

from config import celery_app

User = get_user_model()


@celery_app.task(bind=True)
def send_notification(self, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        devices = FCMDevice.objects.filter(user=notification.user)
        for device in devices:
            response = device.send_message(
                Message(
                    notification=FCMNotification(
                        title=notification.title,
                        body=notification.body,
                        image=notification.image,
                    ),
                    data=notification.data
                )
            )
    except Exception as e:
        self.retry(countdown=10, exc=e)
