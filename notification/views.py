from http import HTTPStatus

from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView


class NotificationListView(APIView):
    def get(self, request: HttpRequest):
        return Response(status=HTTPStatus.OK)
