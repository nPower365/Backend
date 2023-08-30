from itertools import chain
from sre_parse import State
from power_365.authentication.api.serializers import LocationSerializer
from power_365.core.api.serializers import CitySerializer, CountrySerializer, StateSerializer
from power_365.core.models import City, Country
from rest_framework import generics
from power_365.core.api.serializers import SettingSerializer
from power_365.core.models import Setting


class ListSettingView(generics.ListAPIView):
    serializer_class = SettingSerializer
    queryset = Setting.objects.all()
    pagination_class = None
    permission_classes = []


class ListCountries(generics.ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all().order_by('name')
    pagination_class = None
    permission_classes = []
    search_fields = ['name']


class ListStates(generics.ListAPIView):
    serializer_class = StateSerializer
    pagination_class = None
    permission_classes = []
    search_fields = ['name']

    def get_queryset(self):

        return State.objects.filter(country=self.kwargs['country_id'])


class ListCities(generics.ListAPIView):
    serializer_class = CitySerializer
    pagination_class = None
    permission_classes = []
    search_fields = ['name']

    def get_queryset(self):

        return City.objects.filter(state=self.kwargs['state_id'])


class SearchLocations(generics.ListAPIView):
    serializer_class = LocationSerializer
    pagination_class = None
    permission_classes = []

    def get_queryset(self):
        query = self.request.query_params.get('search')
        if not query:
            return Country.objects.all()
        countries = Country.objects.filter(
            name__istartswith=query)
        states = State.objects.filter(
            name__istartswith=query)
        cities = City.objects.filter(
            name__istartswith=query)
        locations = list(chain(countries, states, cities))
        queryset = locations
        return queryset[:50]
