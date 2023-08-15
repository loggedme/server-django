from django.http import HttpRequest
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


@permission_classes([AllowAny])
class AuthTokenView(APIView):
    def post(self, request: HttpRequest):
        pass

    def delete(self, request: HttpRequest):
        pass


@permission_classes([AllowAny])
class AuthValidationView(APIView):
    def post(self, request: HttpRequest):
        pass


@permission_classes([AllowAny])
class AuthValidationCheckView(APIView):
    def post(self, request: HttpRequest):
        pass


@permission_classes([AllowAny])
class AuthResetPasswordView(APIView):
    def post(self, request: HttpRequest):
        pass
