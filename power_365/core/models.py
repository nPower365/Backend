from pyexpat import model
from django.db import models
from django.contrib.auth import get_user_model
from power_365.utils.model_utils import BaseModel
from power_365.utils.enums import MediaType
from power_365.utils.helpers import scramble_uploaded_filename
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Country(BaseModel):
    name = models.CharField(_("Country name"), unique=True, max_length=255)
    iso3 = models.CharField(_("iso3"), null=True, blank=True, max_length=5)
    iso2 = models.CharField(_("iso2"), null=True, blank=True, max_length=5)
    numeric_code = models.CharField(
        _("numeric_code"), max_length=5, blank=True, null=True)
    phone_code = models.CharField(_("Country phone code"),  max_length=255)
    capital = models.CharField(_("Country capital"),
                               max_length=255, null=True, blank=True,)
    currency = models.CharField(
        _("Country currency"),  max_length=255, null=True, blank=True,)
    currency_name = models.CharField(
        _("Country currency_name"),  max_length=255, null=True, blank=True,)
    currency_symbol = models.CharField(
        _("Country currency symbol"),  max_length=255, null=True, blank=True,)
    tld = models.CharField(
        _("Country tld"),  max_length=255, null=True, blank=True,)
    native = models.CharField(
        _("Country native"),  max_length=255, null=True, blank=True,)
    region = models.CharField(
        _("Country region"),  max_length=255, null=True, blank=True,)
    sub_region = models.CharField(
        _("Country sub-region"),  max_length=255, null=True, blank=True,)
    timezones = models.JSONField(
        _("Country timezones"),  max_length=255, null=True, blank=True,)
    translations = models.JSONField(
        _("Country translations"),  max_length=255, null=True, blank=True,)
    latitude = models.CharField(
        _("latitude"), max_length=20, null=True, blank=True)
    longitude = models.CharField(
        _("longitude"), max_length=20, null=True, blank=True,)
    emoji = models.CharField(
        _("Country emoji"),  max_length=255, null=True, blank=True,)
    emojiU = models.CharField(
        _("Country emojiU"),  max_length=255, null=True, blank=True,)
    wikiDataId = models.CharField(_("Country wikiDataId"),
                                  max_length=255, null=True, blank=True,)

    def __str__(self):
        return self.name

    @property
    def location(self):
        return self.name


class State(BaseModel):
    name = models.CharField(_("State name"), unique=True, max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state_code = models.CharField(
        _("state_code"), null=True, blank=True, max_length=5)
    iso2 = models.CharField(_("iso2"), null=True, blank=True, max_length=5)
    type = models.CharField(_("type"), null=True, blank=True, max_length=5)
    latitude = models.CharField(
        _("latitude"), max_length=20, null=True, blank=True,)
    longitude = models.CharField(
        _("longitude"), max_length=20, null=True, blank=True,)

    def __str__(self):
        return self.name

    @property
    def location(self):
        return f'{self.name}, {self.country}'


class City(BaseModel):
    name = models.CharField(_("City name"), unique=True, max_length=255)
    state = models.ForeignKey(
        State, on_delete=models.SET_NULL, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    latitude = models.CharField(
        _("latitude"), max_length=20, null=True, blank=True,)
    longitude = models.CharField(
        _("longitude"), max_length=20, null=True, blank=True,)

    def __str__(self):
        return self.name

    @property
    def location(self):
        return f'{self.name}, {self.state}, {self.country} '


class Media(BaseModel):
    """
    Media model
    """
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="media", blank=True, null=True)
    file = models.FileField(upload_to=scramble_uploaded_filename)
    size = models.IntegerField(default=0)
    type = models.CharField(
        max_length=100, choices=MediaType.choices, default=MediaType.OTHER)
    # extension = models.CharField(max_length=100, default="")
    caption = models.TextField(default="")

    @property
    def extension(self):
        return self.file.name.split(".")[-1]


class Setting(BaseModel):
    key = models.CharField("Setting key", unique=True, max_length=255)
    value = models.CharField("Setting value", max_length=255)

    def save(self, *args, **kwargs):
        self.key = self.key.upper().replace(" ", "_")
        super(Setting, self).save(*args, **kwargs)
