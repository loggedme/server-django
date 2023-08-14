from http import HTTPStatus
from uuid import uuid4

from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User


MOCK_USER = {
    "id": uuid4(),
    "name": "John Doe",
    "handle": "sxvn9wxx",
    "account_type": "personal",
    "thumbnail": "http://...~foo.??"
}

MOCK_JWT = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'


def auth_token(request: HttpRequest) -> HttpResponse:
    user = User.objects.first()
    token = RefreshToken.for_user(user)
    if request.method == 'POST':
        return JsonResponse(status=HTTPStatus.CREATED, data={
            'user': {
                "id": user.id,
                "handle": user.handle,
                "name": user.name,
                "account_type": [None, 'personal', 'business'][user.account_type],
                "thumbnail": "http://...~foo.??"
            },
            "token": str(token.access_token),
        })
    if request.method == 'DELETE':
        return HttpResponse(status=HTTPStatus.OK)
    return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)


def auth_validation(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        return HttpResponse(status=HTTPStatus.OK)
    return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)


def auth_validation_check(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        return HttpResponse(status=HTTPStatus.OK)
    return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)


def auth_reset_password(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        return JsonResponse(status=HTTPStatus.OK, data=MOCK_USER)
    return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)
