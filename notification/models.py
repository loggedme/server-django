from django.db import models

from user.models import User
from feed.models import Post
from badge.models import Badge

# Create your models here.


class NotificationType(models.IntegerChoices):
    LIKE = 1, 'Like'
    FOLLOW = 2, 'Follow'
    COMMENT = 3, 'Comment'
    BADGE = 4, 'Badge'
    TAG = 5, 'Tag'


class Notification(models.Model):
    id = models.UUIDField(primary_key=True)
    type = models.IntegerField(choices=NotificationType.choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
