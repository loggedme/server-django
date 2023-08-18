from typing import Union

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from rest_framework import serializers

from user.models import User
from user.serializers import UserSerializer
from feed.models import *


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(
        source="created_by",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'author',
            'created_at',
        ]


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(
        source='created_by',
        default=serializers.CurrentUserDefault(),
    )
    tagged_user = UserSerializer(read_only=True)
    content = serializers.CharField(
        max_length=2000,
        allow_blank=False,
    )
    image_urls = serializers.SerializerMethodField()
    comment = CommentSerializer(
        source='comment_set',
        many=True,
        read_only=True,
    )
    likes = serializers.SerializerMethodField(read_only=True)
    is_edited = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
    is_saved = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        exclude = ['created_by']

    def _get_current_user(self) -> Union[User, AnonymousUser]:
        if 'request' not in self.context:
            return AnonymousUser()
        request: HttpRequest = self.context['request']
        return request.user

    def get_image_urls(self, obj: Post):
        return [settings.HOSTNAME + o.image.url for o in obj.postimage_set.order_by('order')]

    def get_likes(self, obj: Post):
        return obj.likedpost_set.count()

    def get_is_edited(self, obj: Post):
        return obj.created_at != obj.modified_at

    def get_is_liked(self, obj: Post):
        user = self._get_current_user()
        if user.is_anonymous:
            return False
        return obj.likedpost_set.filter(user=user).exists()

    def get_is_saved(self, obj: Post):
        user = self._get_current_user()
        if user.is_anonymous:
            return False
        return obj.savedpost_set.filter(user=user).exists()
