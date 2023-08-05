from http import HTTPStatus

from django.http import HttpRequest, HttpResponse, JsonResponse


MOCK_USER = {
    "id": "1-sxxx-ajgleja1",
    "name": "John Doe",
    "handle": "sxvn9wxx",
    "account_type": "personal",
    "thumbnail": "http://...~foo.??"
}


def auth_token(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        return JsonResponse(status=HTTPStatus.CREATED, data=MOCK_USER)
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
