from django.views.generic import View
from http import HTTPStatus
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate


from .models import Badge, BadgedUser
from user.models import User

class BadgeApi(View):
    def post(self, request):     # 뱃지 생성
        # if not request.user.is_authenticated:
        #     return HttpResponse(status=401)
        # if request.user.type != "business":
        #     return HttpResponse(status=403)
        #
        # image = request.FILES.get('image')
        # description = request.POST.get('description')
        # if not image or not description:
        #     return HttpResponse(status=400)
        # Badge.objects.create(created_by=request.user.id, image=image, description=description)

        data = {
            "id": "1",
            "thumbnail": "http://...~bar.??",
            "description": "이 뱃지는 1992년 런던에서 시작하여...",
            "publisher": {
                "id": "1-sxxx-ajgleja1",
                "name": "John Doe",
                "handle": "sxvn9wxx",
                "account_type": "personal",
                "thumbnail": "http://...~foo.??"
            }
        }
        return JsonResponse(status=201, data=data)

    def put(self, request, badge_id):      # 뱃지 수정
        # if not request.user.is_authenticated:
        #     return HttpResponse(status=401)
        # if request.user.type != "business":
        #     return HttpResponse(status=403)
        #
        # image = request.FILES.get('image')
        # description = request.POST.get('description')
        # if not image or not description:
        #     return HttpResponse(status=400)

        # Badge.objects.get(id=badge_id)

        data = {
            "id": "1",
            "thumbnail": "http://...~bar.??",
            "description": "이 뱃지는 1992년 런던에서 시작하여...",
            "publisher": {
                "id": "1-sxxx-ajgleja1",
                "name": "John Doe",
                "handle": "sxvn9wxx",
                "account_type": "personal",
                "thumbnail": "http://...~foo.??"
            }
        }
        return JsonResponse(status=200, data=data)

    def delete(self, request, badge_id):   # 뱃지 삭제
        # if not request.user.is_authenticated:
        #     return HttpResponse(status=401)
        # if request.user.type != "business":
        #     return HttpResponse(status=403)
        # if not Badge.objects.filter(id=badge_id).exists():
        #     return HttpResponse(status=404)
        # badge = Badge.objects.get(id=badge_id)
        # badge.delete()

        return HttpResponse(status=200)

class UserBadgeApi(View):
    def get(self, request, user_id):      # 뱃지 리스트 조회
        # if not User.objects.filter(id=user_id):
        #     return HttpResponse(status=404)
        # badge = BadgedUser.objects.filter(user_id=user_id)
        data = {
            {
                "id": "1",
                "thumbnail": "http://...~barwr.??",
                "description": "이 뱃지는 1992년 런던에서 시작하여...",
                "publisher": {
                    "id": "5-sxxx-aryeueja1",
                    "name": "John Doe",
                    "handle": "sxvn9wxxxx",
                    "account_type": "business",
                    "thumbnail": "http://...~fizz.??"
                }
            },
            {
                "id": "11",
                "thumbnail": "http://...~fooo.??",
                "description": "이 뱃지는 1992년 도쿄에서 시작하여...",
                "publisher": {
                    "id": "1-sxxx-ajglrtyr1",
                    "name": "Jane Doe",
                    "handle": "sxvn8ooo",
                    "account_type": "business",
                    "thumbnail": "http://...~foooo.??"
                }
            }
        }
        return JsonResponse(status=200, data=data)

    def post(self, request, user_id, badge_id):     # 뱃지 부여
        # if not request.user.is_authenticated:
        #     return HttpResponse(status=401)
        # if not Badge.objects.filter(id=badge_id).exists():
        #     return HttpResponse(status=404)
        # BadgedUser.objects.create(badge_id=badge_id, user_id=user_id)
        data = {
            "badge": {
                "id": "1",
                "thumbnail": "http://...~bar.??",
                "description": "이 뱃지는 1992년 런던에서 시작하여...",
                "publisher": {
                    "id": "1-sxxx-ajgleja1",
                    "name": "John Doe",
                    "handle": "sxvn9wxx",
                    "account_type": "business",
                    "thumbnail": "http://...~fodo.??"
                }
            },
            "recipient": {
                "id": "5657-sxxx-ajgleja1",
                "name": "Jane Doe",
                "handle": "sxvn9wxxadf",
                "account_type": "personal",
                "thumbnail": "http://...~fafoo.??"
            }
        }
        return JsonResponse(status=201, data=data)

    def delete(self, request, user_id, badge_id):   # 뱃지 회수
        # if not request.user.is_authenticated:
        #     return HttpResponse(status=401)
        # if not BadgedUser.objects.filter(user_id=badge_id, badge_id=badge_id).exists():
        #     return HttpResponse(status=404)
        # badge = BadgedUser.objects.get(badge_id=badge_id, user_id=user_id)
        # badge.delete()

        return HttpResponse(status=200)
