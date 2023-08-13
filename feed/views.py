from typing import Any
from uuid import UUID

from django.http import HttpRequest
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from feed.models import Post
from feed.pagination import simple_pagination
from feed.serializers import PostSerializer


class FeedView(APIView):
    @permission_classes([AllowAny])
    def get(self, request: HttpRequest):
        # TODO: Support Query parameters
        queryset = Post.objects.all()
        page = simple_pagination.paginate_queryset(queryset, request, view=self)
        serializer = PostSerializer(instance=page, many=True)
        return simple_pagination.get_paginated_response(serializer.data)

    def post(self, request: HttpRequest):
        pass


class FeedDetailView(APIView):
    def get(self, request: HttpRequest, post_id: UUID):
        pass

    def put(self, request: HttpRequest, post_id: UUID):
        pass

    def delete(self, request: HttpRequest, post_id: UUID):
        pass


class FeedLikeView(APIView):
    def post(self, request: HttpRequest, post_id: UUID):
        pass

    def delete(self, request: HttpRequest, post_id: UUID):
        pass


class FeedCommentView(APIView):
    def get(self, request: HttpRequest, post_id: UUID):
        pass

    def post(self, request: HttpRequest, post_id: UUID):
        pass


class FeedCommentDetailView(APIView):
    def delete(self, request: HttpRequest, post_id: UUID, comment_id: UUID):
        pass
