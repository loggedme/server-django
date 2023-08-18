import uuid

from django.db import models


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
    arg_comment = models.ForeignKey('feed.Comment', on_delete=models.CASCADE, null=True)
    arg_badge = models.ForeignKey('badge.Badge', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def notify_liked(cls, notified_user, liked_by, post):
        notif = Notification()
        notif.type = NotificationType.LIKE
        notif.notified_user = notified_user
        notif.arg_user = liked_by
        notif.arg_post = post
        notif.save()

    @classmethod
    def notify_followed(cls, notified_user, followed_by):
        notif = Notification()
        notif.type = NotificationType.FOLLOW
        notif.notified_user = notified_user
        notif.arg_user = followed_by
        notif.save()

    @classmethod
    def notify_commented(cls, notified_user, commented_by, comment):
        notif = Notification()
        notif.type = NotificationType.COMMENT
        notif.notified_user = notified_user
        notif.arg_user = commented_by
        notif.arg_post = comment.post
        notif.arg_comment = comment
        notif.save()

    @classmethod
    def notify_badged(cls, notified_user, badged_by, badge):
        notif = Notification()
        notif.type = NotificationType.BADGE
        notif.notified_user = notified_user
        notif.arg_user = badged_by
        notif.arg_badge = badge
        notif.save()

    @classmethod
    def notify_tagged(cls, notified_user, tagged_by, post):
        notif = Notification()
        notif.type = NotificationType.TAG
        notif.notified_user = notified_user
        notif.arg_user = tagged_by
        notif.arg_post = post
        notif.save()
