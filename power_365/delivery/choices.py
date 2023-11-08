from django.db.models import TextChoices


class DeliveryRequestStatuses(TextChoices):
    WAITING = 'waiting', 'waiting'
    PICKED_UP = 'picked up', 'picked up'
    ON_TRANSIT = 'on transit', 'on transit'
    DELIVERED = 'delivered', 'delivered'
