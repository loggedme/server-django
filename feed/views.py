from http import HTTPStatus
from uuid import UUID

from django.http import HttpRequest
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

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
        serializer = PostSerializer(instance=page, many=True)
        return simple_pagination.get_paginated_response(serializer.data)

    def post(self, request: HttpRequest):
        pass


@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([JWTAuthentication])
class FeedDetailView(APIView):
    def get(self, request: HttpRequest, post_id: UUID):
        try:
            entity = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(status=HTTPStatus.NOT_FOUND)
        serializer = PostSerializer(instance=entity)
        return Response(serializer.data, status=HTTPStatus.OK)

    def put(self, request: HttpRequest, post_id: UUID):
        pass

    def delete(self, request: HttpRequest, post_id: UUID):
        pass


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
