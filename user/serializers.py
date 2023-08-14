from rest_framework import serializers

from user.models import User


ACCOUNT_TYPE_MAPPINGS = {
    1: 'personal',
    2: 'business',
}


class UserSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(source='profile_image')
    account_type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'handle',
            'account_type',
            'thumbnail',
        ]

    def get_account_type(self, obj: User):
        return ACCOUNT_TYPE_MAPPINGS[obj.account_type]
