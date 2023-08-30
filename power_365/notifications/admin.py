from django.contrib import admin
from power_365.notifications import models
# Register your models here.


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'date_created')
    search_fields = ('title','user__username')
