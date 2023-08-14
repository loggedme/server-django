from rest_framework import serializers

from user.serializers import UserSerializer
from feed.models import Post, Comment


# TODO: 진짜 썸네일 이미지 URL 매핑하기
CAT_IMAGE_URL = 'https://img.animalplanet.co.kr/news/2021/01/14/700/7xx53252im2gfs7i2ksr.jpg'


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, validated_data):
        raise NotImplementedError()

    def save(self, **kwargs):
        raise NotImplementedError()


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

    def get_image_urls(self, obj: Post):
        return [CAT_IMAGE_URL] * 3

    def get_comment(self, obj: Post):
        return CommentSerializer(obj.comment_set, many=True).data

    def get_likes(self, obj: Post):
        return obj.likedpost_set.count()

    def get_is_edited(self, obj: Post):
        return obj.created_at != obj.modified_at

    def get_is_liked(self, obj: Post):
        return False

    def get_is_saved(self, obj: Post):
        return False
