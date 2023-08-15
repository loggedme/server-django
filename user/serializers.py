from rest_framework import serializers

from user.models import User

class UserSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'password', 'email', 'name', 'handle', 'account_type', 'profile_image', 'thumbnail']
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'write_only': True},
            'password': {'write_only': True},
            'profile_image': {'required': False, 'write_only': True}
        }
        
    def create(self, validated_data):
        return User.objects.create_user(username=validated_data['email'], **validated_data)
    
    def get_thumbnail(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return None 