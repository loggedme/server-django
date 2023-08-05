from http import HTTPStatus

from django.http import HttpRequest, HttpResponse, JsonResponse


MOCK_USER = {
    "id": "1-sxxx-ajgleja1",
    "name": "John Doe",
    "handle": "sxvn9wxx",
    "account_type": "personal",
    "thumbnail": "http://...~foo.??"
}

MOCK_HASHTAG = {
    "name": "우리_빛나는_밤에",
    "feed": {
        "count": 50
    }
}

MOCK_RESPONSE = {
    "user": {
        "count": 3,
        "is_countable": True,
        "page": 1,
        "per_page": 50,
        "items": [MOCK_USER] * 3,
    },
    "hashtag": {
        "count": 10,
        "is_countable": True,
        "page": 1,
        "per_page": 50,
        "items": [MOCK_HASHTAG] * 10,
    }
}


def search(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return JsonResponse(status=HTTPStatus.OK, data=MOCK_RESPONSE)
    return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)
