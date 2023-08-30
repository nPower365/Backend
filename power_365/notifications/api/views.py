from rest_framework.response import Response
from rest_framework import generics
from power_365.notifications.models import Notification
from power_365.notifications.api.serializers import NotificationSerializer, NotificationStatisticsSerializer


class ListNotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):

        return Notification.objects.filter(user=self.request.user)


class RetrieveNotificationView(generics.RetrieveAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.read = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class NotificationStatisticsView(generics.RetrieveAPIView):
    serializer_class = NotificationStatisticsSerializer
    pagination_class = None

    def get_queryset(self):

        return Notification.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        return {
            'unread': queryset.filter(read=False).count(),
            'total': queryset.count()
        }


class MarkUserNotificationsAsRead(generics.CreateAPIView):
    serializer_class = NotificationStatisticsSerializer

    def get_queryset(self):

        return Notification.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        unread_notification = Notification.objects.filter(
            user=self.request.user, read=False)
        if(unread_notification.count() > 0 and unread_notification.update(read=True)):
            return Response({
                'message': 'updated!'
            })

        return Response({'error': f"No notifications to update!" if unread_notification.count() == 0 else 'An error occurred, please try again.'}, 422)
