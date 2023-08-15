from __future__ import annotations

from django.db import models
from django.db.models import QuerySet
from django.contrib.auth.models import AbstractUser

import uuid


class UserType(models.IntegerChoices):
    PERSONAL = 1, 'Personal'
    BUSINESS = 2, 'Business'


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    name = models.CharField(max_length=16, blank=False)
    handle = models.CharField(unique=True, max_length=16, blank=False)
    account_type = models.IntegerField(choices=UserType.choices)
    profile_image =  models.ImageField(upload_to='user_profile_image/', null=True)
    first_name = None
    last_name = None

    followed_user: QuerySet[FollowedUser]
    follower: QuerySet[FollowedUser] # 내가 팔로우 하고 있는 사람들


class FollowedUser(models.Model):
    user = models.ForeignKey(User, related_name='followed_user', on_delete=models.CASCADE)         # 팔로우 받는 사람
    followed_by = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)     # 팔로우 하는 사람

    class Meta:
        unique_together = ['user', 'followed_by']
