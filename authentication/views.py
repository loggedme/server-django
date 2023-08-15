from http import HTTPStatus

from django.http import HttpRequest
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail

from datetime import datetime, timedelta
from user.models import User
from user.serializers import UserSerializer
from .models import EmailValidation


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
        return Response(status=HTTPStatus.OK)


@permission_classes([AllowAny])
class AuthValidationView(APIView):
    def post(self, request: HttpRequest):
        email = request.data.get('email')
        if email is None:
            return Response(status=HTTPStatus.BAD_REQUEST)
        if EmailValidation.objects.filter(email=email).exists():
            EmailValidation.objects.filter(email=email).delete()
        EmailValidationCode = EmailValidation.objects.create(email=email)
        
        subject = 'Logged.me 인증 코드'
        message = EmailValidationCode.code
        from_email = 'loggedme@naver.com'
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return Response(status=HTTPStatus.OK)
        except Exception as e:
            return Response(status=HTTPStatus.SERVICE_UNAVAILABLE)


@permission_classes([AllowAny])
class AuthValidationCheckView(APIView):
    def post(self, request: HttpRequest):
        email = request.data.get('email')
        code = request.data.get('code')
        try:
            mail = EmailValidation.objects.get(email=email)
        except EmailValidation.DoesNotExist:
            return Response(status=HTTPStatus.BAD_REQUEST)
        if code != mail.code:
            return Response(status=HTTPStatus.UNAUTHORIZED)
        return Response(status=HTTPStatus.OK)


@permission_classes([AllowAny])
class AuthResetPasswordView(APIView):
    def post(self, request: HttpRequest):
        email = request.data.get('email')
        code = request.data.get('code')
        password = request.data.get('password')
         
        if password is None or email is None or code is None:
            return Response(status=HTTPStatus.BAD_REQUEST)
        try:
            mail = EmailValidation.objects.get(email=email)
        except EmailValidation.DoesNotExist:
            return Response(status=HTTPStatus.UNAUTHORIZED)
        if code != mail.code:
            return Response(status=HTTPStatus.UNAUTHORIZED)
        if not User.objects.filter(email=email).exists():
            return Response(status=HTTPStatus.BAD_REQUEST)
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        mail.delete()
        return Response(status=HTTPStatus.OK)