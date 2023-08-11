from rest_framework import serializers

from feed.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'content',
            'tagged_user',
            'created_at',
            'modified_at',
            'created_by',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'modified_at',
            'created_by',
        ]
