from django.contrib import admin
from power_365.core import models
# Register your models here.


@admin.register(models.Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'date_created', 'date_modified')
    search_fields = ('key',)


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'capital', 'region')
    search_fields = ('name', 'capital', 'region')


@admin.register(models.State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name', )


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    search_fields = ('name', )
