
import random
import string
import uuid

from power_365.core import models


def scramble_uploaded_filename(instance, filename):
    extension = filename.split(".")[-1]
    return "media/{}.{}".format(uuid.uuid4(), extension)


def get_random_string(size=8, chars=string.ascii_lowercase + string.digits):
    string = ''.join(random.choice(chars) for _ in range(size))
    return string


def get_location(location_id):
    country = models.Country.objects.filter(id=location_id).first()
    if country:
        return country.location
    state = models.State.objects.filter(id=location_id).first()
    if state:
        return state.location
    city = models.City.objects.filter(id=location_id).first()
    return city.location if city else None
