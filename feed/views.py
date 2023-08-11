from uuid import UUID

from django.http import HttpRequest
from rest_framework.views import APIView


class FeedView(APIView):
    def get(self, request: HttpRequest):
        pass

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
