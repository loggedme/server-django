from http import HTTPStatus

from django.http import HttpRequest
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

from datetime import datetime, timedelta
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
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"errors": "no user has this email"}, status=HTTPStatus.UNAUTHORIZED)
        if not check_password(password, user.password):
            return Response({"errors": "wrong password"}, status=HTTPStatus.UNAUTHORIZED)
        token = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
        return Response(
            status=HTTPStatus.CREATED,
            data={
                'token': str(token.access_token),
                'user': serializer.data,
            }
        )

    def delete(self, request: HttpRequest):
         # 로그아웃 시 토큰 무효화 로직
        access_token = request.auth
        refresh_token = RefreshToken(access_token)
    
        # 토큰의 만료 시간을 현재 시간으로부터 2시간 뒤로 조정
        new_expiration = datetime.now() + timedelta(hours=1)
        refresh_token.access_token.set_exp(lifetime=new_expiration - datetime.utcnow())
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
