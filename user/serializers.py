from typing import Union

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from rest_framework import serializers

from user.models import *

class UserSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'password', 'email', 'name', 'handle', 'account_type', 'profile_image', 'thumbnail', 'is_following']
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'write_only': True},
            'password': {'write_only': True},
            'profile_image': {'required': False, 'write_only': True},
        }

    def create(self, validated_data):
        return User.objects.create_user(username=validated_data['email'], **validated_data)

    def get_thumbnail(self, obj):
        if obj.profile_image:
            return settings.HOSTNAME + obj.profile_image.url
        return None

    def get_is_following(self, obj: User):
        user = self._get_current_user()
        if user is None or user.is_anonymous:
            return False
        return user.following.filter(user=obj).exists()

    def _get_current_user(self) -> Union[User, AnonymousUser, None]:
        if 'request' not in self.context:
            return None
        request: HttpRequest = self.context['request']
        return request.user
