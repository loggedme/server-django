from http import HTTPStatus

from django.http import HttpRequest
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User
from user.serializers import UserSerializer


@permission_classes([AllowAny])
class AuthTokenView(APIView):
    def post(self, request: HttpRequest):
        try:
            email = request.data['email']
            password = request.data['password']
        except KeyError:
            return Response(status=HTTPStatus.BAD_REQUEST)
        try:
            user = User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            return Response(status=HTTPStatus.UNAUTHORIZED)
        token = RefreshToken.for_user(user)
        serializer = UserSerializer(instance=user)
        return Response(
            status=HTTPStatus.CREATED,
            data={
                'token': str(token.access_token),
                'user': serializer.data,
            }
        )

    def delete(self, request: HttpRequest):
        # TODO: 토큰 파기 기능 구현
        return Response(status=HTTPStatus.OK)


@permission_classes([AllowAny])
class AuthValidationView(APIView):
    def post(self, request: HttpRequest):
        # TODO: 기능 구현
        return Response(status=HTTPStatus.OK)


@permission_classes([AllowAny])
class AuthValidationCheckView(APIView):
    def post(self, request: HttpRequest):
        # TODO: 기능 구현
        return Response(status=HTTPStatus.OK)


@permission_classes([AllowAny])
class AuthResetPasswordView(APIView):
    def post(self, request: HttpRequest):
        # TODO: 기능 구현
        return Response(status=HTTPStatus.OK)
