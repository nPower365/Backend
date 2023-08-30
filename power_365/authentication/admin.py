from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from power_365.authentication import models
User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ["username", "first_name",
                    "last_name", "is_superuser", 'referral_code']
    search_fields = ('username', 'first_name', 'last_name',
                     'email')


@admin.register(models.Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('id', 'referrer', 'referee')


@admin.register(models.Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'active')
    search_fields = ('user', )
