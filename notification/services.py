from badge.models import Badge
from user.models import User
from feed.models import Post, Comment
from notification.models import *


def notify_like(notified_user: User, liked_by: User, post: Post):
    notif = Notification()
    notif.type = NotificationType.LIKE
    notif.notified_user = notified_user
    notif.arg_user = liked_by
    notif.arg_post = post
    notif.save()


def notify_follow(notified_user: User, followed_by: User):
    notif = Notification()
    notif.type = NotificationType.FOLLOW
    notif.notified_user = notified_user
    notif.arg_user = followed_by
    notif.save()


def notify_comment(notified_user: User, commented_by: User, comment: Comment):
    notif = Notification()
    notif.type = NotificationType.COMMENT
    notif.notified_user = notified_user
    notif.arg_user = commented_by
    notif.arg_post = comment.post
    notif.arg_comment = comment
    notif.save()


def notify_badge(notified_user: User, badged_by: User, badge: Badge):
    notif = Notification()
    notif.type = NotificationType.BADGE
    notif.notified_user = notified_user
    notif.arg_user = badged_by
    notif.arg_badge = badge
    notif.save()


def notify_tag(notified_user: User, tagged_by: User, post: Post):
    notif = Notification()
    notif.type = NotificationType.TAG
    notif.notified_user = notified_user
    notif.arg_user = tagged_by
    notif.arg_post = post
    notif.save()
