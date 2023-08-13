from rest_framework import serializers

from user.models import User
from feed.models import Post, Comment


# TODO: 진짜 썸네일 이미지 URL 매핑하기
CAT_IMAGE_URL = 'https://img.animalplanet.co.kr/news/2021/01/14/700/7xx53252im2gfs7i2ksr.jpg'
ACCOUNT_TYPE_MAPPINGS = {
    1: 'personal',
    2: 'business',
}


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, validated_data):
        raise NotImplementedError()

    def save(self, **kwargs):
        raise NotImplementedError()


class UserSerializer(serializers.ModelSerializer):
    account_type = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'handle',
            'account_type',
            'thumbnail',
        ]
        read_only_fields = [
            'id',
            'account_type',
        ]

    def get_account_type(self, obj: User):
        return ACCOUNT_TYPE_MAPPINGS[obj.account_type]

    def get_thumbnail(self, obj: User):
        return CAT_IMAGE_URL


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'author',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'author',
            'created_at',
        ]

    def get_author(self, obj: Post):
        return UserSerializer(obj.created_by).data


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    tagged_user = UserSerializer()
    image_urls = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    is_edited = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'tagged_user',
            'content',
            'image_urls',
            'comment',
            'likes',
            'created_at',
            'modified_at',
            'is_liked',
            'is_saved',
            'is_edited',
        ]
        read_only_fields = [
            'id',
            'author',
            'comment',
            'likes',
            'created_at',
            'modified_at',
            'is_liked',
            'is_saved',
            'is_edited',
        ]

    def get_author(self, obj: Post):
        return UserSerializer(obj.created_by).data

    def get_image_urls(self, obj: Post):
        return [CAT_IMAGE_URL] * 3

    def get_comment(self, obj: Post):
        return CommentSerializer(obj.comment_set, many=True).data

    def get_likes(self, obj: Post):
        return 0

    def get_is_edited(self, obj: Post):
        return obj.created_at != obj.modified_at

    def get_is_liked(self, obj: Post):
        return False

    def get_is_saved(self, obj: Post):
        return False
