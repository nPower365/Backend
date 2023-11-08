from django.urls import path
from power_365.delivery.api.views import (
    delivery_request,
    list_create_delivery_request,
    list_deliveries,
    delivery
)
app_name = "wallets"

urlpatterns = [
    path("deliveries/", view=list_create_delivery_request, name="deliveries"),
    path("deliveries/<pk>", view=delivery, name="delivery"),
    path("delivery-requests/", view=list_deliveries, name="delivery_requests"),
    path("delivery-requests/<pk>", view=delivery_request, name="delivery_request"),
]
