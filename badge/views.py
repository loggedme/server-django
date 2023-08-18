from http import HTTPStatus

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response

from user.models import User, UserType
from user.serializers import UserSerializer
from badge.models import Badge, BadgedUser
from badge.serializers import BadgeSerializer
from notification.services import notify_badge

class BadgeCreateView(generics.CreateAPIView):
    serializer_class = BadgeSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        self_badge = BadgedUser.objects.create(badge_id=serializer.data['id'], user_id=self.request.user.id)
        self_badge.save()

    def create(self, request):
        if request.user.is_anonymous:
            return Response(status=HTTPStatus.UNAUTHORIZED)
        if request.user.account_type != UserType.BUSINESS:
            return Response(status=HTTPStatus.FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTPStatus.CREATED, headers=headers)

class BadgeUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BadgeSerializer
    permission_classes = [permissions.AllowAny]

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
        if request.user.is_anonymous:
            return Response(status=HTTPStatus.UNAUTHORIZED)
        if request.user.account_type != UserType.BUSINESS:
            return Response(status=HTTPStatus.FORBIDDEN)
        badge = get_object_or_404(Badge, id=badge_id)
        if badge.created_by != request.user:
            return Response(status=HTTPStatus.FORBIDDEN)
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, badge_id, *args, **kwargs):
        return self.patch(request, badge_id, *args, **kwargs)

    def destroy(self, request, badge_id):
        if request.user.is_anonymous:
            return Response(status=HTTPStatus.UNAUTHORIZED)
        if request.user.account_type != UserType.BUSINESS:
            return Response(status=HTTPStatus.FORBIDDEN)
        badge = get_object_or_404(Badge, id=badge_id)
        if badge.created_by != request.user:
            return Response(status=HTTPStatus.FORBIDDEN)
        self.perform_destroy(badge)
        return Response(status=HTTPStatus.OK)

class BadgedUserCreateDeleteView(generics.GenericAPIView):
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, **kwargs):
        badge = get_object_or_404(Badge, id=kwargs["badge_id"])
        if request.user.account_type != UserType.BUSINESS or badge.created_by != request.user:
            return Response(status=HTTPStatus.FORBIDDEN)
        user_ids = request.data.get('users')
        user_list = []

        for user_id in user_ids:
            try:
                user = User.objects.get(id=user_id)
                badged_user = BadgedUser(user=user, badge=badge)
                badged_user.save()
                user_list.append(user)
                notify_badge(notified_user=badged_user.user, badged_by=request.user, badge=badged_user.badge)
            except (User.DoesNotExist, IntegrityError):
                continue

        badge_serializer = self.get_serializer(badge)
        self.serializer_class = UserSerializer
        recipient_serializer = self.get_serializer(user_list, many=True)
        data = {
            "badge": badge_serializer.data,
            "recipient": { "items": recipient_serializer.data }
        }

        return Response(data, status=HTTPStatus.CREATED)

    def delete(self, request, badge_id):
        badge = get_object_or_404(Badge, id=badge_id)
        if request.user.account_type != UserType.BUSINESS or badge.created_by != request.user:
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
