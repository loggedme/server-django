import json
from django.views.generic import View
from http import HTTPStatus
from django.http import JsonResponse, HttpResponse, HttpRequest
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


class BadgeUserApi(View):
    def post(self, request: HttpRequest, badge_id):
        try:
            data = json.loads(request.body)
            assert 'users' in data
        except:
            return HttpResponse(status=400)
        return HttpResponse(status=201)

    def delete(self, request, badge_id):
        try:
            data = json.loads(request.body)
            assert 'users' in data
        except:
            return HttpResponse(status=400)
        return HttpResponse(status=200)
