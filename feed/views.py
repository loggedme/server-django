import json
from http import HTTPStatus
from uuid import UUID
from typing import List

from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import generics, views, status
from rest_framework.exceptions import ValidationError, NotAuthenticated, PermissionDenied
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User, UserType
from user.services import get_user
from feed.pagination import simple_pagination, SimplePagination
from feed.models import *
from feed.serializers import *


class FeedListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    pagination_class = SimplePagination

    def get_queryset(self):
        queryset = Post.objects.order_by('-created_at')
        queryset = self._filter_queryset_type(queryset)
        queryset = self._filter_queryset_following(queryset)
        queryset = self._filter_queryset_trending(queryset)
        queryset = self._filter_queryset_hashtag(queryset)
        return queryset

    def _filter_queryset_type(self, queryset: QuerySet[Post]) -> QuerySet[Post]:
        raw_type = self.request.GET.get('type')
        if raw_type is None:
            return queryset
        for key, value in UserType.choices:
            if value.lower() == raw_type:
                return queryset.filter(created_by__account_type=key)
        raise ValidationError(f'"{raw_type}" is not a valid type. choices are ["personal", "business"]')

    def _filter_queryset_following(self, queryset: QuerySet[Post]) -> QuerySet[Post]:
        raw_following = self.request.GET.get('following')
        if raw_following is None:
            return queryset
        if raw_following == 'false':
            raise ValidationError('exclude followings is not supported.')
        if raw_following != '' and raw_following != 'true':
            raise ValidationError(f'"following={raw_following}" is invalid')
        if not self.request.user.is_authenticated:
            raise NotAuthenticated()
        user: User = self.request.user
        following_ids = user.following.values_list('user', flat=True)
        return queryset.filter(created_by__id__in=following_ids)

    def _filter_queryset_trending(self, queryset: QuerySet[Post]) -> QuerySet[Post]:
        if self.request.GET.get('trending', 'false') == 'false':
            return queryset
        return queryset.order_by('-likedpost')

    def _filter_queryset_hashtag(self, queryset: QuerySet[Post]) -> QuerySet[Post]:
        raw_hashtag = self.request.GET.get('hashtag')
        if raw_hashtag is None:
            return queryset
        if raw_hashtag != raw_hashtag.strip():
            raise ValidationError("spaces are not allowed for hashtag")
        if raw_hashtag == '':
            raise ValidationError("empty hashtag is not allowed")
        post_ids = HashTaggedPost.objects.filter(hashtag__name=raw_hashtag).values_list('post', flat=True)
        return queryset.filter(id__in=post_ids)

    def perform_create(self, serializer: PostSerializer):
        images = self.request.FILES.getlist('images')
        if len(images) == 0 or len(images) > 10:
            raise ValidationError(f'{len(images)} images are not allowed.')
        kwargs = {}
        if 'tagged_user' in self.request.data:
            try:
                user_id = UUID(self.request.data['tagged_user'])
                kwargs['tagged_user'] = User.objects.get(id=user_id)
            except ValueError as e:
                raise ValidationError(e)
            except User.DoesNotExist:
                raise ValidationError({
                    "message": f"User with id '{user_id}' is not found.",
                })
        with transaction.atomic():
            post = serializer.save(**kwargs)
            for order, image in enumerate(images):
                postimage = PostImage()
                postimage.post = post
                postimage.image = image
                postimage.order = order
                postimage.save()


class FeedDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects
    lookup_url_kwarg = 'post_id'

    def check_object_permissions(self, request: HttpRequest, obj: Post):
        if request.method != 'GET' and obj.created_by != request.user:
            raise PermissionDenied({
                "message": "자신이 작성한 피드만 수정하거나 삭제 할 수 있습니다.",
                "author": obj.created_by.handle,
                "currentUser": request.user.handle,
            })
        return super().check_object_permissions(request, obj)

    def perform_update(self, serializer: PostSerializer):
        kwargs = {}
        if 'tagged_user' in self.request.data:
            try:
                user_id = UUID(self.request.data['tagged_user'])
                kwargs['tagged_user'] = User.objects.get(id=user_id)
            except ValueError as e:
                raise ValidationError(e)
            except User.DoesNotExist:
                raise ValidationError({
                    "message": f"User with id '{user_id}' is not found.",
                })
        serializer.save(**kwargs)


class FeedLikeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return LikedPost.objects

    def post(self, request: HttpRequest, **kwargs):
        obj, created = self.get_queryset().get_or_create(user=request.user, **kwargs)
        return Response(status=status.HTTP_202_ACCEPTED if not created else status.HTTP_205_RESET_CONTENT)

    def delete(self, request: HttpRequest, **kwargs):
        obj, created = self.get_queryset().get_or_create(user=request.user, **kwargs)
        obj.delete()
        return Response(status=status.HTTP_202_ACCEPTED if created else status.HTTP_205_RESET_CONTENT)


class FeedSaveView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        return SavedPost.objects

    def post(self, request: HttpRequest, **kwargs):
        obj, created = self.get_queryset().get_or_create(user=request.user, **kwargs)
        return Response(status=status.HTTP_202_ACCEPTED if not created else status.HTTP_205_RESET_CONTENT)

    def delete(self, request: HttpRequest, **kwargs):
        obj, created = self.get_queryset().get_or_create(user=request.user, **kwargs)
        obj.delete()
        return Response(status=status.HTTP_202_ACCEPTED if created else status.HTTP_205_RESET_CONTENT)


class CommentListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    pagination_class = SimplePagination
    queryset = Comment.objects

    def get_queryset(self):
        return super().get_queryset().filter(**self.kwargs)

    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs['post_id'])


class CommentDetailsView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    queryset = Comment.objects
    lookup_url_kwarg = 'comment_id'

    def perform_destroy(self, instance: Comment):
        if self.request.user != instance.created_by:
            raise PermissionDenied('자신이 작성한 댓글만 삭제할 수 있습니다.')
        return super().perform_destroy(instance)
