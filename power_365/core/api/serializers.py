from dataclasses import field
from power_365.core.models import City, Country, State
from rest_framework import serializers
from config.settings.base import ALLOWED_AUDIO_TYPE, ALLOWED_DOCUMENT_TYPE, ALLOWED_IMAGE_TYPE, ALLOWED_VIDEO_TYPE
from power_365.core import models
from django.contrib.auth import get_user_model
from power_365.utils.utils import get_media_type
User = get_user_model()


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = "__all__"


class StateSerializer(serializers.ModelSerializer):
    country = serializers.StringRelatedField()

    class Meta:
        model = State
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    state = serializers.StringRelatedField()
    country = serializers.StringRelatedField()

    class Meta:
        model = City
        fields = "__all__"


class MediaSerializer(serializers.ModelSerializer):
    extension = serializers.CharField(read_only=True)

    class Meta:
        model = models.Media
        fields = ('id', 'file', 'extension', 'caption')

    def create(self, validated_data):
        media = super().create(validated_data)
        # media.extension = media.media.name.split('.')[-1]
        media.size = media.file.size
        media.type = get_media_type(media.extension)
        media.save()

    def validate(self, data):
        if 'media' not in data:
            raise serializers.ValidationError('Media is required')

        if data.get('media').size > 5000000:
            raise serializers.ValidationError(
                'File size must be less than 5MB')

        file_extension = data.get('media').filename.split('.')[-1]
        if file_extension not in ALLOWED_AUDIO_TYPE + ALLOWED_DOCUMENT_TYPE + ALLOWED_IMAGE_TYPE + ALLOWED_VIDEO_TYPE:
            raise serializers.ValidationError('Unsupported Media Format')
        return data


class SettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Setting
        fields = ['key', 'value']
