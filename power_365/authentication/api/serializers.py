from tokenize import String
from pkg_resources import require
from power_365.core.api.serializers import MediaSerializer
from djoser.conf import settings as djoser_settings
from rest_framework import serializers
from djoser.serializers import UserCreatePasswordRetypeSerializer
from power_365.authentication.models import *
from power_365.core.models import *
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt import exceptions
from django.utils.translation import gettext_lazy as _
from djoser.serializers import UidAndTokenSerializer
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import exceptions as drf_exceptions

User = get_user_model()


class ProfileImageSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=False, read_only=True)

    class Meta:
        model = ProfileImage
        fields = ('id', 'media', 'extension',
                  'caption')

    def create(self, validated_data):
        media = self.context.get('media')
        media = Media.objects.create(
            user=self.context['user'], file=media)
        profile_image = ProfileImage.objects.create(
            user=self.context['user'], media=media, **validated_data)
        return profile_image


class CustomRegisterSerializer(UserCreatePasswordRetypeSerializer):

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    referral_code = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)
        user = super().create(validated_data)
        if referral_code:
            referrer = User.objects.filter(referral_code=referral_code).first()
            if referrer:
                user.referrer = referrer
                user.save()
                Referral.objects.create(
                    referrer=referrer,
                    referee=user
                )

        return user

    class Meta:
        model = UserCreatePasswordRetypeSerializer.Meta.model
        fields = UserCreatePasswordRetypeSerializer.Meta.fields + \
            ("first_name", "last_name", "gender", "date_of_birth", 'referral_code')
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }



class TokenObtainSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD

    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username_or_email'] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs['username_or_email'],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError(
            'Must implement `get_token` method for `TokenObtainSerializer` subclasses')


class CustomActivationSerializer(UidAndTokenSerializer):
    default_error_messages = {
        "stale_token": djoser_settings.CONSTANTS.messages.STALE_TOKEN_ERROR
    }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not self.user.is_email_verified:
            return attrs
        raise drf_exceptions.PermissionDenied(
            self.error_messages["stale_token"])


class CustomTokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = UserSerializer(self.user).data

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data



class UserSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()
    state = serializers.StringRelatedField()
    city = serializers.StringRelatedField()
    username = serializers.CharField(max_length=255, required=False)
    current_profile_image = ProfileImageSerializer(read_only=True)


    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all()
    )
    state_id = serializers.PrimaryKeyRelatedField(
        queryset=State.objects.all()
    )
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all()
    )


    def update(self, instance, validated_data):
        country_id = validated_data.pop(
            "country_id", instance.country.id if instance.country else None)
        state_id = validated_data.pop(
            "state_id", instance.state.id if instance.state else None)
        city_id = validated_data.pop(
            "city_id", instance.city.id if instance.city else None)
        phone_number = validated_data.pop(
            "phone_number", instance.phone_number)

        instance.country = country_id if not isinstance(
            country_id, str) else Country.objects.filter(id=country_id).first()
        instance.state = state_id if not isinstance(
            state_id, str) else State.objects.filter(id=state_id).first()
        instance.city = city_id if not isinstance(
            city_id, str)else City.objects.filter(id=city_id).first()
        instance.phone_number = phone_number
        instance.first_name = validated_data.get(
            "first_name", instance.first_name)
        instance.last_name = validated_data.get(
            "last_name", instance.last_name)
        instance.last_name = validated_data.get(
            "other_name", instance.other_name)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.date_of_birth = validated_data.get(
            "date_of_birth", instance.date_of_birth)


        instance.save()
        return instance


    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "name",
            "email",
            "gender",
            "date_of_birth",
            "phone_number",
            "current_profile_image",
            "country",
            "state",
            "city",
            'country_id',
            'state_id',
            'city_id',
            'is_active',
            'referral_code',
            'online',
            'is_verified',
            "date_joined"]


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source="key")
    user = UserSerializer(read_only=True)

    class Meta:
        model = djoser_settings.TOKEN_MODEL
        fields = ('auth_token', 'user')



class SetPinSerializer(serializers.Serializer):
    old_pin = serializers.CharField(max_length=4, required=False)
    pin = serializers.CharField(max_length=4)
    pin_confirmation = serializers.CharField(max_length=6)


class VerifyPinSerializer(serializers.Serializer):
    pin = serializers.CharField(max_length=4)


class LocationSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255)
