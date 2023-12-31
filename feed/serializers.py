from typing import Union

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from rest_framework import serializers

from user.models import User
from user.serializers import UserSerializer
from feed.models import *


# TODO: 진짜 썸네일 이미지 URL 매핑하기
CAT_IMAGE_URL = 'https://img.animalplanet.co.kr/news/2021/01/14/700/7xx53252im2gfs7i2ksr.jpg'


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(source="created_by")

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
    )
    tagged_user = UserSerializer(
        allow_null=True,
    )
    image_urls = serializers.SerializerMethodField()
    comment = CommentSerializer(
        source='comment_set',
        many=True,
    )
    likes = serializers.SerializerMethodField()
    is_edited = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

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
