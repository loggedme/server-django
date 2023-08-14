from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
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
    tagged_user = UserSerializer()
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

    user: AbstractBaseUser | AnonymousUser

    def __init__(self, user: AbstractBaseUser | AnonymousUser, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.user = user

    def get_image_urls(self, obj: Post):
        return [o.image.url for o in obj.postimage_set.order_by('order')]

    def get_likes(self, obj: Post):
        return obj.likedpost_set.count()

    def get_is_edited(self, obj: Post):
        return obj.created_at != obj.modified_at

    def get_is_liked(self, obj: Post):
        return not self.user.is_anonymous and self.is_liked_by(obj, self.user)

    def is_liked_by(self, post: Post, user: User) -> bool:
        try:
            post.likedpost_set.get(user=user)
        except LikedPost.DoesNotExist:
            return False
        return True

    def get_is_saved(self, obj: Post):
        return not self.user.is_anonymous and self.is_saved_by(obj, self.user)

    def is_saved_by(self, post: Post, user: User) -> bool:
        try:
            post.savedpost_set.get(user=user)
        except SavedPost.DoesNotExist:
            return False
        return True
