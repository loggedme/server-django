from http import HTTPStatus

from django.http import HttpRequest
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


@permission_classes([AllowAny])
@authentication_classes([JWTAuthentication])
class SearchView(APIView):
    def get(self, request: HttpRequest):
        return Response(status=HTTPStatus.OK)
