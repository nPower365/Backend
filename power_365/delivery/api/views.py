from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from power_365.delivery import models
from power_365.delivery.api import serializers
from rest_framework.exceptions import ParseError
from rest_framework import status
from power_365.delivery.choices import DeliveryRequestStatuses

class ListCreateDeliveryRequest(generics.ListAPIView):
    serializer_class = serializers.DeliveryRequestSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return models.DeliveryRequest.objects.filter(user=self.request.user)

list_create_delivery_request = ListCreateDeliveryRequest.as_view()


class DeliveryRequestDetail(generics.RetrieveAPIView):
    serializer_class = serializers.DeliveryRequestSerializer
    queryset = models.DeliveryRequest.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.DeliveryRequest.objects.filter(user=self.request.user)

delivery_request = DeliveryRequestDetail.as_view()




class ListDeliveries(generics.ListAPIView):
    serializer_class = serializers.DeliveryRequestSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return models.DeliveryRequest.objects.filter(agent=self.request.user)

list_deliveries = ListDeliveries.as_view()


class DeliveryDetail(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.DeliveryRequestSerializer
    queryset = models.DeliveryRequest.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.DeliveryRequest.objects.filter(agent=self.request.user)

    def update(self, request, *args, **kwargs):
        _status = kwargs.get('status')
        _obj = self.get_object()
        if not status:
            raise ParseError(detail="Status is required",
                         code=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if status == DeliveryRequestStatuses.PICKED_UP:
            if _obj.status == DeliveryRequestStatuses.PICKED_UP:
                raise ParseError(detail="Item has been picked up already.",
                         code=status.HTTP_422_UNPROCESSABLE_ENTITY)

            # create an activity
            activity = models.DeliveryActivity.objects.create(
                delivery_request=_obj,
                user=self.request.user,
                action=DeliveryRequestStatuses.PICKED_UP,
                description='Item has been picked up buy an agent'
            )
            return super().update(request, *args, **kwargs)

        if status == DeliveryRequestStatuses.ON_TRANSIT:
            if _obj.status == DeliveryRequestStatuses.ON_TRANSIT:
                raise ParseError(detail="Item is already on transit.",
                         code=status.HTTP_422_UNPROCESSABLE_ENTITY)

            # create an activity
            activity = models.DeliveryActivity.objects.create(
                delivery_request=_obj,
                user=self.request.user,
                action=DeliveryRequestStatuses.ON_TRANSIT,
                description='Item is on transit'
            )
            return super().update(request, *args, **kwargs)

        if status == DeliveryRequestStatuses.DELIVERED:
            code = kwargs.get('pickup_code')

            if not code:
                raise ParseError(detail="Pickup code is required.",
                         code=status.HTTP_422_UNPROCESSABLE_ENTITY)

            if _obj.status == DeliveryRequestStatuses.DELIVERED:
                raise ParseError(detail="Item has been delivered already.",
                         code=status.HTTP_422_UNPROCESSABLE_ENTITY)

            if code != _obj.pickup_code:
                raise ParseError(detail="Pickup code is incorrect.",
                         code=status.HTTP_422_UNPROCESSABLE_ENTITY)

            # create an activity
            activity = models.DeliveryActivity.objects.create(
                delivery_request=_obj,
                user=self.request.user,
                action=DeliveryRequestStatuses.DELIVERED,
                description='Item has been delivered'
            )
            return super().update(request, *args, **kwargs)

delivery = DeliveryDetail.as_view()
