from rest_framework import serializers

from feed.models import HashTag


class HashTagSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    feed = serializers.SerializerMethodField()

    class Meta:
        model = HashTag
        fields = ['name', 'feed']

    def get_feed(self, obj: HashTag):
        return {
            "count": obj.hashtaggedpost_set.count(),
        }
