from http import HTTPStatus

from django.http import HttpRequest, HttpResponse, JsonResponse


MOCK_USER = {
    "id": "1-sxxx-ajgleja1",
    "name": "John Doe",
    "handle": "sxvn9wxx",
    "account_type": "personal",
    "thumbnail": "http://...~foo.??"
}

MOCK_JWT = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'


def auth_token(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        return HttpResponse(status=HTTPStatus.CREATED, content=MOCK_JWT)
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
