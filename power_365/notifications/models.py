from django.contrib.auth import get_user_model
from django.db import models
from power_365.utils.model_utils import BaseModel
from power_365.utils.choices import NotificationTypes
User = get_user_model()


class Notification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.URLField(null=True, blank=True)
    data = models.JSONField(blank=True, null=True)
    read = models.BooleanField(default=False)
    type = models.CharField(
        max_length=255, choices=NotificationTypes.choices, default=NotificationTypes.NOTIFICATION)

    def __str__(self):
        return self.user.username + ' ' + self.type

    class Meta:
        ordering = ['-date_created']
