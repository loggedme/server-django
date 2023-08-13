from __future__ import annotations

from uuid import uuid4
from django.db import models

from user.models import User

# Create your models here.


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    content = models.CharField(max_length=2000)
    tagged_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='tagged_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    comment_set: models.QuerySet[Comment]
    savedpost_set: models.QuerySet[SavedPost]
    likedpost_set: models.QuerySet[LikedPost]
    postimage_set: models.QuerySet[PostImage]


class PostImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    order = models.IntegerField()
    image = models.FileField(upload_to='post/images')


class LikedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class HashTag(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=False)

    hashtaggedpost_set: models.QuerySet[HashTaggedPost]


class HashTaggedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(HashTag, on_delete=models.CASCADE)
