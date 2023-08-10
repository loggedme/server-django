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

MOCK_SIMPLIFIED_POST = {
    "id": "1",
    "author": MOCK_USER,
    "image_urls": [
        "http://...~bar.??",
        "http://...~foo.??",
        "http://...~faz.??"
    ],
}

MOCK_BADGE = {
    "id": "1",
    "thumbnail": "http://...~bar.??",
    "description": "이 뱃지는 1992년 런던에서 시작하여...",
    "publisher": MOCK_USER,
}

MOCK_RESPONSE = {
    "count": 5,
    "is_countable": True,
    "page": 1,
    "per_page": 50,
    "items": [
        {
            "type": "like",
            "user": MOCK_USER,
            "feed": MOCK_SIMPLIFIED_POST,
            "comment": None,
            "badge": None,
            "created_at": "2023-08-01T12:31:12.456"
        },
        {
            "type": "follow",
            "user": MOCK_USER,
            "feed": None,
            "comment": None,
            "badge": None,
            "created_at": "2023-08-01T12:31:12.456"
        },
        {
            "type": "badge",
            "user": MOCK_USER,
            "feed": None,
            "comment": None,
            "badge": MOCK_BADGE,
            "created_at": "2023-08-01T12:31:12.456"
        },
        {
            "type": "tag",
            "user": MOCK_USER,
            "feed": MOCK_SIMPLIFIED_POST,
            "comment": None,
            "badge": None,
            "created_at": "2023-08-01T12:31:12.456"
        },
        {
            "type": "comment",
            "user": MOCK_USER,
            "feed": MOCK_SIMPLIFIED_POST,
            "comment": MOCK_COMMENT,
            "badge": None,
            "created_at": "2023-08-01T12:31:12.456"
        }
    ]
}


def notification(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        return JsonResponse(status=HTTPStatus.OK, data=MOCK_RESPONSE)
    return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)
