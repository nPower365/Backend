from django.urls import path, include
from power_365.notifications.api.views import ListNotificationsView, MarkUserNotificationsAsRead, NotificationStatisticsView, RetrieveNotificationView
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('devices', FCMDeviceAuthorizedViewSet)


app_name = "notifications"

urlpatterns = [
    path('notifications/', include(router.urls)),
    path('notifications/mark-as-read',
         MarkUserNotificationsAsRead.as_view(), name='mark-as-read'),
    path('notification-statistics/', NotificationStatisticsView.as_view(),
         name="notification-statistics"),
    path("account/notifications/", ListNotificationsView.as_view(),
         name="list_notifications"),
    path("account/notifications/<str:pk>/", RetrieveNotificationView.as_view(),
         name="single_notifications"),
]
