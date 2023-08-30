from rest_framework import serializers
from power_365.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class NotificationStatisticsSerializer(serializers.Serializer):
    unread = serializers.IntegerField()
    total = serializers.IntegerField()
