from django.urls import path

from power_365.core.api.views import ListSettingView
from power_365.core.api.views import ListCities, ListCountries, ListStates, SearchLocations


app_name = "core"
urlpatterns = [
    path("app-settings/", ListSettingView.as_view(), name="list_app_settings"), path("locations/",
                                                                                     SearchLocations.as_view(), name="locations"),
    path("locations/countries/",
         ListCountries.as_view(), name="Countries"),
    path("locations/countries/<str:country_id>/states/",
         ListStates.as_view(), name="states"),
    path("locations/states/<str:state_id>/cities/",
         ListCities.as_view(), name="cities"),

]
