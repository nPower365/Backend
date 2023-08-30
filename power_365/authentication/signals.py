from locale import currency
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from power_365.core.models import Level
from power_365.authentication.models import Follow
from power_365.authentication.tasks import create_new_follow_notification
User = get_user_model()


