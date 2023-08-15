from rest_framework import serializers
from django.conf import settings
from .models import Badge
from user.models import User
from user.serializers import UserSerializer

class BadgeSerializer(serializers.ModelSerializer):
    publisher = UserSerializer(source="created_by", read_only=True)
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Badge
        fields = ['id', 'description', 'image', 'thumbnail', 'publisher']
        extra_kwargs = {
            'id': {'read_only': True},
            'image': {'write_only': True, 'required': True},
        }

    def create(self, validated_data):
        badge = Badge.objects.create(**validated_data)
        return badge

    def get_thumbnail(self, obj):
        return settings.HOSTNAME + obj.image.url
