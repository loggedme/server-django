from django.db import models

# Create your models here.


class UserType(models.IntegerChoices):
    PERSONAL = 1, 'Personal'
    BUSINESS = 2, 'Business'


class User(models.Model):
    id = models.UUIDField(primary_key=True)
    email = models.EmailField(unique=True, max_length=64)
    password = models.CharField(max_length=16, blank=False)
    name = models.CharField(max_length=16, blank=False)
    handle = models.CharField(unique=True, max_length=16, blank=False)
    account_type = models.IntegerField(choices=UserType.choices)
    profile_image = models.Field()
    created_at = models.DateTimeField(auto_now_add=True)
    last_logged_in = models.DateTimeField(null=True)

class FollowedUser(models.Model):
    user_id = models.ForeignKey(User, related_name='followed_user', on_delete=models.CASCADE)         # 팔로우 받는 사람
    followed_by = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)     # 팔로우 하는 사람

    class Meta:
        unique_together = ['user_id', 'followed_by']
