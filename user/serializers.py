from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
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
        request: HttpRequest = self.context['request']
        if request is None:
            raise NotImplementedError()
        user: AbstractBaseUser | AnonymousUser | User = request.user
        if user is None:
            raise NotImplementedError()
        if user.is_anonymous:
            return False
        try:
            user.follower.get(user=obj)
            return True
        except FollowedUser.DoesNotExist:
            return False
        return False
