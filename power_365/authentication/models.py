
from decimal import Decimal
import random
import string
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from power_365.utils import  choices
from power_365.utils.model_utils import BaseModel


def generate_referral_code(size=8, chars=string.ascii_lowercase + string.digits):
    while True:
        string = ''.join(random.choice(chars) for _ in range(size))
        return string
        if not User.objects.filter(referral_code=string).first():
            return string


class User(AbstractUser):
    """
    Default custom user model for Fidle Backend.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True, serialize=False, verbose_name='ID')
    first_name = models.CharField(
        _("First name of User"), blank=True, max_length=255)
    last_name = models.CharField(
        _("Last name of User"), blank=True, max_length=255)
    other_name = models.CharField(
        _("Other name of User"), blank=True, max_length=255)
    password = models.CharField(max_length=128, null=True, blank=True)
    date_of_birth = models.DateField(_("Date of birth"), null=True, blank=True)
    gender = models.CharField(_("Gender"), max_length=20,
                              choices=choices.GenderType.choices, null=True, blank=True)
    country = models.ForeignKey(
        'core.Country', on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(
        'core.State', on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(
        'core.City', on_delete=models.SET_NULL, null=True, blank=True)
    verified_at = models.DateTimeField(_("Verified at"), null=True, blank=True)

    referral_code = models.CharField(
        max_length=10, null=True, blank=True, default=generate_referral_code)
    referrer = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    phone_number = models.CharField(
        _("Phone number"), max_length=20, null=True, blank=True)
    online = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_joined']

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        return self.username


    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def name(self):
        """
        Return the user's full name.

        Returns:
            str: User's full name.

        """
        return self.get_full_name()


    @property
    def is_verified(self):
        """Check if user is verified.

        Returns:
            bool: True if user is verified, False otherwise.

        """
        return self.verified_at is not None

    @property
    def age(self):
        return self.date_of_birth.year - self.date_of_birth.today().year if self.date_of_birth else 18

    @property
    def has_pin(self):
        return self.pins.filter(active=True).exists()
# fix for circular import

    class Meta:
        ordering = ["-date_joined"]




class ProfileImage(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="profile_images")
    media = models.OneToOneField(
        "core.Media", on_delete=models.CASCADE, related_name="profile_image")
    caption = models.CharField(max_length=255, blank=True, null=True)
    is_current = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    @property
    def extension(self):
        return self.media.name.split('.')[-1]


class Pin(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='pins', blank=True, null=True)
    code = models.CharField(_("code"), max_length=255)
    active = models.BooleanField(default=True)


class Referral(BaseModel):
    referrer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='referrers')
    referee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='referees')
