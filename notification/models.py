import uuid

from django.db import models

# Create your models here.


class NotificationType(models.IntegerChoices):
    LIKE = 1, 'Like'
    FOLLOW = 2, 'Follow'
    COMMENT = 3, 'Comment'
    BADGE = 4, 'Badge'
    TAG = 5, 'Tag'


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.IntegerField(choices=NotificationType.choices)
    notified_user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='notifications')
    arg_user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True)
    arg_post = models.ForeignKey('feed.Post', on_delete=models.CASCADE, null=True)
    arg_badge = models.ForeignKey('badge.Badge', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
