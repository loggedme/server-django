from django.views.generic import View
from http import HTTPStatus
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout

from .models import User, FollowedUser
from badge.models import Badge, BadgedUser
from feed.models import Post


def user_detail_or_search(self, request, user_id):  # 사용자 조회 / query parameter 있으면 사용자 검색
    type = request.GET.get('type')
    query = request.GET.get('query')
    recommend = request.GET.get('recommend')
    if type and query:  # 검색
        if type == "business":
            data = {
                "count": 1,
                "is_countable": True,
                "page": 1,
                "per_page": 50,
                "items": [
                    {
                        "id": "1-sxxx-ajgleja1",
                        "name": "John Doe",
                        "handle": "sxvn9wxx",
                        "account_type": "business",
                        "thumbnail": "http://...~foo.??"
                    }
                ]
            }
            return JsonResponse(status=200, data=data)

        elif type == "personal":
            data = {
                "count": 1,
                "is_countable": True,
                "page": 1,
                "per_page": 50,
                "items": [
                    {
                        "id": "1-sxxx-ajgleja1",
                        "name": "John Doe",
                        "handle": "sxvn9wxx",
                        "account_type": "business",
                        "thumbnail": "http://...~foo.??"
                    }
                ]
            }
            return JsonResponse(status=200, data=data)

        return HttpResponse(status=400)
    if recommend:   # 태그 추천
        if type == "business":
            data = {
                "count": 5,
                "is_countable": True,
                "page": 1,
                "per_page": 50,
                "items": [
                    {
                        "id": "1-sxxx-ajgleja1",
                        "name": "John Doe1",
                        "handle": "sxvn9wxx1",
                        "account_type": "business",
                        "thumbnail": "http://...~foo1.??"
                    },
                    {
                        "id": "1-sxxx-ajgleja2",
                        "name": "John Doe2",
                        "handle": "sxvn9wxx2",
                        "account_type": "business",
                        "thumbnail": "http://...~foo2.??"
                    },
                    {
                        "id": "1-sxxx-ajgleja3",
                        "name": "John Doe3",
                        "handle": "sxvn9wxx3",
                        "account_type": "business",
                        "thumbnail": "http://...~foo3.??"
                    },
                    {
                        "id": "1-sxxx-ajgleja4",
                        "name": "John Doe4",
                        "handle": "sxvn9wxx4",
                        "account_type": "business",
                        "thumbnail": "http://...~foo4.??"
                    },
                    {
                        "id": "1-sxxx-ajgleja5",
                        "name": "John Doe5",
                        "handle": "sxvn9wxx5",
                        "account_type": "business",
                        "thumbnail": "http://...~foo5.??"
                    }
                ]
            }
            return JsonResponse(status=200, data=data)
        elif type == "personal":
            data = {
                "count": 5,
                "is_countable": True,
                "page": 1,
                "per_page": 50,
                "items": [
                    {
                        "id": "1-sxxx-ajgleja1",
                        "name": "John Doe1",
                        "handle": "sxvn9wxx1",
                        "account_type": "personal",
                        "thumbnail": "http://...~foo1.??"
                    },
                    {
                        "id": "1-sxxx-ajgleja2",
                        "name": "John Doe2",
                        "handle": "sxvn9wxx2",
                        "account_type": "personal",
                        "thumbnail": "http://...~foo2.??"
                    },
                    {
                        "id": "1-sxxx-ajgleja3",
                        "name": "John Doe3",
                        "handle": "sxvn9wxx3",
                        "account_type": "personal",
                        "thumbnail": "http://...~foo3.??"
                    },
                    {
                        "id": "1-sxxx-ajgleja4",
                        "name": "John Doe4",
                        "handle": "sxvn9wxx4",
                        "account_type": "personal",
                        "thumbnail": "http://...~foo4.??"
                    },
                    {
                        "id": "1-sxxx-ajgleja5",
                        "name": "John Doe5",
                        "handle": "sxvn9wxx5",
                        "account_type": "personal",
                        "thumbnail": "http://...~foo5.??"
                    }
                ]
            }
            return JsonResponse(status=200, data=data)
        elif not type:
            data = {
                "count": 5,
                "is_countable": True,
                "page": 1,
                "per_page": 50,
                "items": [
                    {
                        "id": "1-sxxx-ajgleja1",
                        "name": "John Doe1",
                        "handle": "sxvn9wxx1",
                        "account_type": "personal",
                        "thumbnail": "http://...~foo1.??"
                    },
                    {
                        "id": "1-sxxx-ajgleja2",
                        "name": "John Doe2",
                        "handle": "sxvn9wxx2",
                        "account_type": "business",
                        "thumbnail": "http://...~foo2.??"
                    },
                    {
                        "id": "1-sxxx-ajgleja3",
                        "name": "John Doe3",
                        "handle": "sxvn9wxx3",
                        "account_type": "personal",
                        "thumbnail": "http://...~foo3.??"
                    },
                    {
                        "id": "1-sxxx-ajgleja4",
                        "name": "John Doe4",
                        "handle": "sxvn9wxx4",
                        "account_type": "business",
                        "thumbnail": "http://...~foo4.??"
                    },
                    {
                        "id": "1-sxxx-ajgleja5",
                        "name": "John Doe5",
                        "handle": "sxvn9wxx5",
                        "account_type": "personal",
                        "thumbnail": "http://...~foo5.??"
                    }
                ]
            }
            return JsonResponse(status=200, data=data)
        return HttpResponse(status=400)

    if User.objects.filter(id=user_id).exists():    # 사용자 조회
        data = {
            "user": {
                "id": "1-sxxx-ajgleja1",
                "name": "John Doe",
                "handle": "sxvn9wxx",
                "account_type": "personal",
                "thumbnail": "http://...~foo.??"
            },
            "badge": {
                "items": [
                    {
                        "id": "1",
                        "thumbnail": "http://...~foo.??",
                        "description": "이 뱃지는 1992년 런던에서 시작하여...",
                        "publisher": {
                            "id": "1-sxxx-ajgleja1",
                            "name": "John Doe",
                            "handle": "sxvn9wxx",
                            "account_type": "business",
                            "thumbnail": "http://...~foo.???"
                        },
                    },
                    {
                        "id": "2",
                        "thumbnail": "http://...~bar.??",
                        "description": "이 뱃지는 1993년 도쿄에서 시작하여...",
                        "publisher": {
                            "id": "2-sxxx-afda1",
                            "name": "Jane Doe",
                            "handle": "asdfaf5454",
                            "account_type": "business",
                            "thumbnail": "http://...~bar.???"
                        },
                    }
                ]
            },
            "follow": {
                "following": 181,
                "follower": 172
            }
        }
        return JsonResponse(status=200, data=data)
    else:
        return HttpResponse(status=404)


# noinspection PyMethodMayBeStatic
class UserApi(View):
    def post(self, request):     # 사용자 회원 가입
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        handle = request.POST.get('handle')
        account_type = request.POST.get('account_type')

        if not email or not password or not name or not handle or not account_type:
            return HttpResponse(status=400)

        if User.objects.filter(email=email).exists() or User.objects.filter(handle=handle).exists():
            return HttpResponse(status=409)

        # user = User.objects.create_user(
        #     email=email, password=password,
        #     name=name, handle=handle, account_type=account_type
        # )

        return JsonResponse(status=201, data={
          "id": "1-sxxx-ajgleja1",
          "name": "John Doe",
          "handle": "sxvn9wxx",
          "account_type": "personal",
          "thumbnail": "http://...~foo.??"
        })

    def put(self, request, user_id):      # 사용자 정보 수정
        name = request.POST.get('name')
        handle = request.POST.get('handle')
        profile_image = request.POST.get('profile_image')

        if not name or not handle:
            return HttpResponse(status=400)

        if request.user == User.objects.get(id=user_id):
            return HttpResponse(status=401)

        return JsonResponse(status=200, data={
          "id": "1-sxxx-ajgleja1",
          "name": "John Doe",
          "handle": "sxvn9wxx",
          "account_type": "personal",
          "thumbnail": "http://...~foo.??"
        })

    def delete(self, request, user_id):   # 사용자 회원 탈퇴
        if request.user == User.objects.get(id=user_id):
            request.user.delete()
            return HttpResponse(status=200)

        return HttpResponse(status=401)

# noinspection PyMethodMayBeStatic
class FollowApi(View):
    def get(self, request, user_id):      # 팔로잉 조회
        if not request.user.is_authenticated:
            return HttpResponse(stauts=401)
        if not User.objects.filter(id=user_id).exists():
            return HttpResponse(status=404)

        data = {
            "count": 2,
            "is_countable": True,
            "page": 1,
            "per_page": 50,
            "items": [
                {"id": "1-sxxx-ajgleja1", "name": "John Doe", "handle": "sxvn9wxx",
                 "account_type": "personal", "thumbnail": "http://...~foo.??"},
                {"id": "uuid-1", "name": "Jane Doe", "handle": "hepxheir",
                 "account_type": "business", "thumbnail": "http://.../thumbnail.jpg"}
            ]
        }
        return JsonResponse(status=200, data=data)

    def post(self, request, user_id, following):     # user_id가 followed_id를 팔로우 하기
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        if not User.objects.filter(id=following).exists():
            return HttpResponse(status=404)

        FollowedUser.objects.create(user_id=user_id, followed_by=following)
        data = {"user": {
            "id": "1-sxxx-ajgleja1",
            "name": "John Doe",
            "handle": "sxvn9wxx",
            "account_type": "personal",
            "thumbnail": "http://...~foo.??"
            },
            "following": {
                "id": "5-sxxx-fweafds1",
                "name": "Jane Doe",
                "handle": "asdfasdf1234",
                "account_type": "business",
                "thumbnail": "http://...~foo.??"
            }
        }
        return JsonResponse(status=201, data=data)

    def delete(self, request, user_id, following):   # user_id가 followed_id를 팔로우 끊기
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        if not User.objects.filter(id=following).exists():
            return HttpResponse(status=404)

        follow = FollowedUser.objects.get(user_id=user_id, followed_by=following)
        follow.delete()

        return HttpResponse(status=200)

def follower_list_api(request, user_id):  # 팔로워 조회
    if not request.user.is_authenticated:
        return HttpResponse(stauts=401)
    if not User.objects.filter(id=user_id).exists():
        return HttpResponse(status=404)

    data = {
        "count": 2,
        "is_countable": True,
        "page": 1,
        "per_page": 50,
        "items": [
            {"id": "1-sxxx-ajgleja1", "name": "John Doe", "handle": "sxvn9wxx",
             "account_type": "personal", "thumbnail": "http://...~foo.??"},
            {"id": "uuid-1", "name": "Jane Doe", "handle": "hepxheir",
             "account_type": "business", "thumbnail": "http://.../thumbnail.jpg"}
        ]
    }
    return JsonResponse(status=200, data=data)

# noinspection PyMethodMayBeStatic
class SavedPostApi(View):
    def get(self, request, user_id):      # 저장한 게시물 조회
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        # data = SavedPost.objects.filter(user_id=user_id)
        data = {
            "count": 1,
            "is_countable": True,
            "page": 1,
            "per_page": 50,
            "items": [
                {
                    "id": "1",
                    "author": {
                        "id": "1-sxxx-aqreleja1",
                        "name": "John Doe",
                        "handle": "sxvn9wxx",
                        "account_type": "personal",
                        "thumbnail": "http://...~foo.??"
                    },
                    "image_urls": [
                        "http://...~bar.??",
                        "http://...~foo.??",
                        "http://...~faz.??"
                    ]
                }
            ]
        }
        return JsonResponse(status=200, data=data)

    def post(self, request, user_id, feed_id):  # 게시물 저장
        # SavedPost.objects.create(user_id=user_id, post_id=feed_id)
        if not request.user.is_authenticated:
            return HttpResponse(stauts=401)
        if not Post.objects.filter(id=feed_id).exists():
            return HttpResponse(status=404)

        data = {
            "id": "1",
            "content": "안녕하세요",
            "image_urls": [
                "http://...~bar.??",
                "http://...~foo.??",
                "http://...~faz.??"
            ],
            "tagged_user": {
                "id": "1-sxxx-ajgleja1",
                "name": "John Doe",
                "handle": "sxvn9wxx",
                "account_type": "business",
                "thumbnail": "http://...~foo.??"
            },
            "created_at": "2023-08-01T19:30:15.123",
            "modified_at": "2023-08-01T19:30:15.123",
            "is_edited": False,
            "author": {
                "id": "1-sxxx-ajgleja2",
                "name": "John Doe2",
                "handle": "sxvn9wxx2",
                "account_type": "personal",
                "thumbnail": "http://...~foo.??"
            },
            "likes": 100,
            "is_liked": False,
            "is_saved": True,
            "comment": {
                "count": 20,
                "items": [
                    {
                        "content": "안녕하세요",
                        "author": {
                            "id": "1-sxxx-ajgleja3",
                            "name": "John Doe3",
                            "handle": "sxvn9wxx3",
                            "account_type": "personal",
                            "thumbnail": "http://...~foo.??"
                        },
                        "created_at": "YYYY-MM-DDThh:mm:ss.xxx"
                    },
                    {
                        "content": "반갑습니다",
                        "author": {
                            "id": "1-sxxx-ajgleja4",
                            "name": "John Doe4",
                            "handle": "sxvn9wxx4",
                            "account_type": "personal",
                            "thumbnail": "http://...~foo.??"
                        },
                        "created_at": "YYYY-MM-DDThh:mm:ss.xxx"
                    }
                ]
            }
        }
        return JsonResponse(status=201, data=data)

    def delete(self, request, user_id, feed_id):   # 게시물 저장 취소
        # post = SavedPost.objects.get(user_id=user_id, post_id=feed_id)
        if not request.user.is_authenticated:
            return HttpResponse(stauts=401)
        if not Post.objects.filter(id=feed_id).exists():
            return HttpResponse(status=404)
        # post.delete()

        return HttpResponse(status=200)

