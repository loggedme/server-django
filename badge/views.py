from http import HTTPStatus
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from user.models import User, UserType
from badge.models import Badge, BadgedUser
from .serializers import BadgeSerializer
from user.serializers import UserSerializer

from rest_framework import generics, permissions

class BusinessUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False
        return user.account_type == UserType.BUSINESS

class BadgeCreateView(generics.CreateAPIView):
    serializer_class = BadgeSerializer
    permission_classes = [BusinessUserPermission]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class BadgeUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BadgeSerializer
    permission_classes = [BusinessUserPermission]

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        return self.permission_classes

    def get_object(self):
        badge_id = self.kwargs['badge_id']
        try:
            obj = Badge.objects.get(id=badge_id)
        except Badge.DoesNotExist:
            return Response(status=HTTPStatus.NOT_FOUND)
        return obj

    def retrieve(self, request, badge_id):
        badge = get_object_or_404(Badge, id=badge_id)
        serializer = self.get_serializer(badge)
        return Response(serializer.data)

    def patch(self, request, badge_id, *args, **kwargs):
        badge = get_object_or_404(Badge, id=badge_id)
        if badge.created_by != request.user:
            return Response(status=HTTPStatus.FORBIDDEN)
        return self.partial_update(request, *args, **kwargs)

    def destroy(self, request, badge_id):
        badge = get_object_or_404(Badge, id=badge_id)
        if badge.created_by != request.user:
            return Response(status=HTTPStatus.FORBIDDEN)
        self.perform_destroy(badge)
        return Response(status=HTTPStatus.OK)

class BadgedUserCreateDeleteView(generics.GenericAPIView):
    serializer_class = BadgeSerializer
    permission_classes = [BusinessUserPermission]

    def post(self, request, **kwargs):
        badge = get_object_or_404(Badge, id=kwargs["badge_id"])
        if badge.created_by != request.user:
            return Response(status=HTTPStatus.FORBIDDEN)
        user_ids = request.data.get('users')
        user_list = []

        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)
                badged_user = BadgedUser(user=user, badge=badge)
                badged_user.save()
                user_list.append(user)
            except (User.DoesNotExist, IntegrityError):
                continue

        badge_serializer = BadgeSerializer(badge)
        recipient_serializer = UserSerializer(user_list, many=True)
        data = {
            "badge": badge_serializer.data,
            "recipient": { "items": recipient_serializer.data }
        }

        return Response(data, status=HTTPStatus.CREATED)

    def delete(self, request, badge_id):
        badge = get_object_or_404(Badge, id=badge_id)
        if badge.created_by != request.user:
            return Response(status=HTTPStatus.FORBIDDEN)
        user_ids = request.data.get('users', [])

        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)
                badged_user = BadgedUser.objects.get(user=user, badge=badge)
                badged_user.delete()
            except (User.DoesNotExist, BadgedUser.DoesNotExist):
                pass

        return Response(status=HTTPStatus.OK)
