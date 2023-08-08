from http import HTTPStatus

from django.http import HttpRequest, HttpResponse, JsonResponse


MOCK_USER = {
    "id": "1-sxxx-ajgleja1",
    "name": "John Doe",
    "handle": "sxvn9wxx",
    "account_type": "personal",
    "thumbnail": "http://...~foo.??"
}

MOCK_COMMENT = {
    "id": "aibje-xxlej-139vlaje",
    "content": "안녕하세요",
    "author": MOCK_USER,
    "created_at": "YYYY-MM-DDThh:mm:ss.xxx"
}

MOCK_COMMENTS = {
    "count": 10,
    "is_countable": True,
    "page": 1,
    "per_page": 50,
    "items": [MOCK_COMMENT] * 10,
}

MOCK_POST = {
    "id": "1",
    "content": "안녕하세요",
    "image_urls": [
        "http://...~bar.??",
        "http://...~foo.??",
        "http://...~faz.??"
    ],
    "tagged_user": MOCK_USER,
    "created_at": "2023-08-01T19:30:15.123",
    "modified_at": "2023-08-01T19:30:15.123",
    "is_edited": False,
    "author": MOCK_USER,
    "likes": 0,
    "is_liked": False,
    "is_saved": False,
    "comment": {
        "count": 24,
        "is_countable": True,
        "page": 1,
        "per_page": 2,
        "items": [MOCK_COMMENT] * 2,
    }
}

MOCK_POSTS = {
    "count": 10,
    "is_countable": True,
    "page": 1,
    "per_page": 50,
    "items": [MOCK_POST] * 10,
}

def post(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return JsonResponse(status=HTTPStatus.OK, data=MOCK_POSTS)
    if request.method == 'POST':
        return JsonResponse(status=HTTPStatus.CREATED, data=MOCK_POST)
    return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)


def post_id(request: HttpRequest, post_id: str) -> HttpResponse:
    if request.method == 'GET':
        return JsonResponse(status=HTTPStatus.OK, data=MOCK_POST)
    if request.method == 'PUT':
        return JsonResponse(status=HTTPStatus.OK, data=MOCK_POST)
    if request.method == 'DELETE':
        return HttpResponse(status=HTTPStatus.OK)
    return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)


def post_id_like(request: HttpRequest, post_id: str) -> HttpResponse:
    if request.method == 'PUT':
        return JsonResponse(status=HTTPStatus.OK, data=MOCK_POST)
    if request.method == 'DELETE':
        return JsonResponse(status=HTTPStatus.OK, data=MOCK_POST)
    return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)


def post_id_comment(request: HttpRequest, post_id: str) -> HttpResponse:
    if request.method == 'GET':
        return JsonResponse(status=HTTPStatus.OK, data=MOCK_COMMENTS)
    if request.method == 'POST':
        return JsonResponse(status=HTTPStatus.CREATED, data=MOCK_COMMENT)
    return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)


def post_id_comment_id(request: HttpRequest, post_id: str, comment_id: str) -> HttpResponse:
    if request.method == 'DELETE':
        return HttpResponse(status=HTTPStatus.OK)
    return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)
