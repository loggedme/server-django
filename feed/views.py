import json
from http import HTTPStatus
from uuid import UUID
from typing import List

from django.db import transaction
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User, UserType
from feed.pagination import simple_pagination
from feed.models import *
from feed.serializers import *


@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([JWTAuthentication])
class FeedView(APIView):
    def get(self, request: HttpRequest):
        # TODO: Support Query parameters
        queryset = Post.objects.all()
        page = simple_pagination.paginate_queryset(queryset, request, view=self)
        serializer = PostSerializer(user=request.user, instance=page, many=True)
        return simple_pagination.get_paginated_response(serializer.data)

    def post(self, request: HttpRequest):
        # TODO: 누락된 키가 있을 경우 예외처리
        user: User = request.user
        images = request.FILES.getlist('images')
        with transaction.atomic():
            post = Post()
            post.content = request.data['content']
            post.created_by = user
            if user.account_type == UserType.PERSONAL:
                try:
                    post.tagged_user = self.get_user_by_id_or_handle(request.data['tagged_user'])
                except User.DoesNotExist as e:
                    return Response(data={'tagged_user': e.args}, status=HTTPStatus.BAD_REQUEST)
            elif user.account_type == UserType.BUSINESS:
                post.tagged_user = None
            else:
                raise Exception()
            post.save()
            for order, image in enumerate(images):
                postimage = PostImage()
                postimage.post = post
                postimage.image = image
                postimage.order = order
                postimage.save()
        serializer = PostSerializer(user=request.user, instance=post)
        return Response(serializer.data, status=HTTPStatus.CREATED)

    def get_user_by_id_or_handle(self, id_or_handle: str) -> User:
        kwargs = {}
        if self.is_uuid(id_or_handle):
            kwargs['id'] = UUID(id_or_handle)
        else:
            kwargs['handle'] = id_or_handle
        return User.objects.get(**kwargs)

    def is_uuid(self, uuid_to_test: str) -> bool:
        try:
            uuid_obj = UUID(uuid_to_test)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_to_test


@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([JWTAuthentication])
class FeedDetailView(APIView):
    def get(self, request: HttpRequest, post_id: UUID, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(user=request.user, instance=post)
        return Response(serializer.data, status=HTTPStatus.OK)

    def put(self, request: HttpRequest, post_id: UUID, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        user: User = request.user
        data = json.loads(request.body)
        if post.created_by != user:
            return Response(status=HTTPStatus.FORBIDDEN)
        with transaction.atomic():
            post.content = data['content']
            if user.account_type == UserType.PERSONAL:
                try:
                    post.tagged_user = self.get_user_by_id_or_handle(data['tagged_user'])
                except User.DoesNotExist as e:
                    return Response(data={'tagged_user': e.args}, status=HTTPStatus.BAD_REQUEST)
            elif user.account_type == UserType.BUSINESS:
                post.tagged_user = None
            else:
                raise Exception()
            post.save()
            # TODO: 새로운 이미지 추가
            image_urls: List[str] = data['image_urls']
            for postimage in post.postimage_set.all():
                try:
                    postimage.order = image_urls.index(postimage.image.url)+1
                    postimage.save()
                except ValueError:
                    print(postimage.image.url, 'not found from', image_urls)
                    postimage.delete()
        serializer = PostSerializer(user=request.user, instance=post)
        return Response(serializer.data, status=HTTPStatus.OK)

    def delete(self, request: HttpRequest, post_id: UUID, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        if post.created_by != request.user:
            return Response(status=HTTPStatus.FORBIDDEN)
        post.delete()
        return Response(status=HTTPStatus.OK)

    def get_user_by_id_or_handle(self, id_or_handle: str) -> User:
        kwargs = {}
        if self.is_uuid(id_or_handle):
            kwargs['id'] = UUID(id_or_handle)
        else:
            kwargs['handle'] = id_or_handle
        return User.objects.get(**kwargs)

    def is_uuid(self, uuid_to_test: str) -> bool:
        try:
            uuid_obj = UUID(uuid_to_test)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_to_test


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
class FeedLikeView(APIView):
    def post(self, request: HttpRequest, post_id: UUID):
        LikedPost.objects.get_or_create(post_id=post_id, user_id=request.user.id)
        return Response(status=HTTPStatus.CREATED)

    def delete(self, request: HttpRequest, post_id: UUID):
        LikedPost.objects.get(post_id=post_id, user_id=request.user.id).delete()
        return Response(status=HTTPStatus.OK)


@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([JWTAuthentication])
class FeedCommentView(APIView):
    @permission_classes([AllowAny])
    def get(self, request: HttpRequest, post_id: UUID):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(status=HTTPStatus.NOT_FOUND)
        queryset = post.comment_set.all()
        page = simple_pagination.paginate_queryset(queryset, request, view=self)
        serializer = CommentSerializer(
            instance=page,
            many=True,
        )
        return simple_pagination.get_paginated_response(serializer.data)

    def post(self, request: HttpRequest, post_id: UUID):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(status=HTTPStatus.NOT_FOUND)
        if 'content' not in request.data:
            return Response(status=HTTPStatus.BAD_REQUEST)
        comment = post.comment_set.create(
            content=request.data['content'],
            created_by=request.user,
        )
        return Response(CommentSerializer(instance=comment).data, status=HTTPStatus.CREATED)


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
class FeedCommentDetailView(APIView):
    def delete(self, request: HttpRequest, post_id: UUID, comment_id: UUID):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response(status=HTTPStatus.NOT_FOUND)
        if comment.created_by != request.user:
            return Response(status=HTTPStatus.FORBIDDEN)
        return Response(status=HTTPStatus.OK)
