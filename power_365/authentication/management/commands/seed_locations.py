import json
import os

# import requests
from django.core.management.base import BaseCommand

from power_365.core.models import City, Country, State


def seed_country_states_and_cities():
    path = os.getcwd() + "/power_365/utils/jsons/location-seeder.json"
    with open(path) as f:
        data = json.load(f)
        for country in data:
            new_country = Country.objects.filter(name=country.get("name")).first()
            if not new_country:
                new_country = Country.objects.create(
                    name=country.get("name"),
                    iso3=country.get("iso3"),
                    iso2=country.get("iso2"),
                    numeric_code=country.get("numeric_code"),
                    phone_code=country.get("phone_code"),
                    capital=country.get("capital"),
                    currency=country.get("currency"),
                    currency_name=country.get("currency_name"),
                    currency_symbol=country.get("currency_symbol"),
                    tld=country.get("tld"),
                    native=country.get("native"),
                    region=country.get("region"),
                    sub_region=country.get("subregion"),
                    timezones=country.get("timezones"),
                    translations=country.get("translations"),
                    latitude=country.get("latitude"),
                    longitude=country.get("longitude"),
                    emoji=country.get("emoji"),
                    emojiU=country.get("emojiU"),
                )
            for state in country.get("states"):
                new_state = State.objects.filter(name=state.get("name")).first()
                if not new_state:
                    new_state = State.objects.create(
                        name=state.get("name"),
                        country=new_country,
                        state_code=state.get("state_code"),
                        latitude=state.get("latitude"),
                        longitude=state.get("longitude"),
                    )

                for city in state.get("cities"):
                    new_city = City.objects.filter(name=city.get('name')).first()
                    if not new_city:
                        new_city = City.objects.create(name=city.get('name'),
                                                       latitude=state.get("latitude"),
                                                       longitude=state.get("longitude"), state=new_state, country=new_country)


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Seeding countries, states and cities...")
        seed_country_states_and_cities()
        print("completed")
