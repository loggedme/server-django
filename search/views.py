from http import HTTPStatus

from django.http import HttpRequest
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User
from user.serializers import UserSerializer
from feed.models import HashTag
from feed.pagination import simple_pagination
from search.serializers import HashTagSerializer


@permission_classes([AllowAny])
@authentication_classes([JWTAuthentication])
class SearchView(APIView):
    def get(self, request: HttpRequest):
        try:
            query = request.GET['query']
        except KeyError:
            return Response(status=HTTPStatus.BAD_REQUEST)
        return Response(
            status=HTTPStatus.OK,
            data={
                'user': self._search_user(request, query).data,
                'hashtag': self._search_hashtag(request, query).data,
            }
        )

    def _search_user(self, request: HttpRequest, query: str):
        queryset = User.objects.filter(handle__startswith=query)
        page = simple_pagination.paginate_queryset(queryset, request, self)
        serializer = UserSerializer(page, many=True)
        return simple_pagination.get_paginated_response(serializer.data)

    def _search_hashtag(self, request: HttpRequest, query: str):
        queryset = HashTag.objects.filter(name__startswith=query)
        page = simple_pagination.paginate_queryset(queryset, request, self)
        serializer = HashTagSerializer(page, many=True)
        return simple_pagination.get_paginated_response(serializer.data)
