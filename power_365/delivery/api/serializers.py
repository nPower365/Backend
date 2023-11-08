from random import randint
from rest_framework import serializers
from power_365.delivery import models
from power_365.delivery.choices import DeliveryRequestStatuses
class PickupSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Pickup
        fields = "__all__"

class DeliveryRequestSerializer(serializers.ModelSerializer):
    pickup = PickupSerializer()
    status = serializers.ChoiceField(DeliveryRequestStatuses.choices)

    def create(self, validated_data):

        # generate pickup_code
        validated_data['pickup_code'] = randint(1000,9999)
        return super().create(validated_data)

    class Meta:
        model = models.DeliveryRequest
        fields = "__all__"

