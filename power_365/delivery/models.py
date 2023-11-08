from django.db import models

from power_365.utils.model_utils import BaseModel
from power_365.delivery import choices

from django.contrib.auth import get_user_model
User = get_user_model()

class DeliveryRequest(BaseModel):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    product_description = models.TextField(blank=True, null=True)
    pickup_code = models.CharField(max_length=32)
    status = models.CharField(max_length=255, choices=choices.DeliveryRequestStatuses.choices, default=choices.DeliveryRequestStatuses.WAITING)
    agent = models.ForeignKey(User,
                             on_delete=models.SET_NULL, null=True, blank=True, related_name="agent")

    def __str__(self):
        return self.code

class Pickup(BaseModel):
    first_name = models.CharField(max_length=32)
    family_name = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    email = models.EmailField(max_length=32)
    delivery_request = models.ForeignKey(DeliveryRequest, on_delete=models.CASCADE)

class DeliveryActivity(BaseModel):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    delivery_request = models.ForeignKey(DeliveryRequest,
                             on_delete=models.CASCADE)
    action = models.CharField(max_length=255, choices=choices.DeliveryRequestStatuses.choices)
    description = models.CharField(max_length=255)



