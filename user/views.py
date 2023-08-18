from http import HTTPStatus

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from authentication.models import EmailValidation
from badge.models import Badge, BadgedUser
from badge.serializers import BadgeSerializer
from feed.models import Post, SavedPost
from feed.pagination import SimplePagination
from feed.serializers import PostSerializer
from user.models import FollowedUser, User
from user.serializers import UserSerializer


class UserPagenation(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'per_page'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'is_countable': True,
            'page': self.page.number,
            'per_page': self.page.paginator.per_page,
            'items': data
        })

class UserDetailUpdateDeleteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserSerializer

    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=HTTPStatus.NOT_FOUND)

    def get(self, request, user_id):
        user = self.get_object(user_id)
        badge_ids = BadgedUser.objects.filter(user=user).values_list('badge_id', flat=True)
        badges = Badge.objects.filter(id__in=badge_ids)
        following_num = FollowedUser.objects.filter(followed_by=user).count()
        follower_num = FollowedUser.objects.filter(user=user).count()
        posts = Post.objects.filter(created_by=user).order_by('-created_at')
        user_serializer = self.get_serializer(user)
        self.serializer_class = BadgeSerializer
        badge_serializer = self.get_serializer(badges, many=True)
        self.serializer_class = PostSerializer
        feed_serializer = self.get_serializer(instance=posts, many=True)

        data = {
            "user": user_serializer.data,
            "badge": {"items": badge_serializer.data},
            "feed": {"count": posts.count(), "items": feed_serializer.data},
            "following": following_num,
            "follower": follower_num
        }
        return Response(data, status=HTTPStatus.OK)

    def patch(self, request, user_id):
        user = self.get_object(user_id)
        if request.user.id != user_id:
            return Response(status=HTTPStatus.FORBIDDEN)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

    def put(self, request, user_id):
        return self.patch(request, user_id)

    def delete(self, request, user_id):
        user = self.get_object(user_id)
        if request.user != user:
            return Response(status=HTTPStatus.FORBIDDEN)
        user.delete()

        return Response(status=HTTPStatus.OK)

class UserSignupSearchView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    pagination_class = UserPagenation

    def get(self, request):
        type = self.request.query_params.get('type')
        query = self.request.query_params.get('query')
        recommend = self.request.query_params.get('recommend')

        if recommend:   # 태그 추천
            self.permission_classes = [permissions.IsAuthenticated]
            if type == "business":
                users = User.objects.annotate(
                    follower_count=Count('follower', distinct=True)
                    ).filter(account_type=2).order_by('-follower_count')[:5]
            elif type == "personal":
                users = User.objects.annotate(
                    follower_count=Count('follower', distinct=True)
                    ).filter(account_type=1).order_by('-follower_count')[:5]
            elif not type:
                users = User.objects.annotate(
                    follower_count=Count('follower', distinct=True)
                    ).order_by('-follower_count')[:5]
        elif type and query:  # 검색
            if type == "business":
                users = User.objects.filter(Q(name__icontains=query) | Q(handle__icontains=query), account_type=2)
            elif type == "personal":
                users = User.objects.filter(Q(name__icontains=query) | Q(handle__icontains=query), account_type=1)
        else:
            return Response(status=HTTPStatus.BAD_REQUEST)

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=HTTPStatus.OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        email = request.data.get('email')
        code = request.data.get('code')
        if not EmailValidation.objects.filter(email=email, code=code).exists():
            return Response(status=HTTPStatus.UNAUTHORIZED)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
        self.perform_create(serializer)
        EmailValidationCode = EmailValidation.objects.get(email=email, code=code)
        EmailValidationCode.delete()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTPStatus.CREATED, headers=headers)

class FollowingListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = UserPagenation

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        following_ids = FollowedUser.objects.filter(followed_by=user).values_list('user_id', flat=True)
        users = User.objects.filter(id__in=following_ids)
        return users

class FollowerListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = UserPagenation

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        following_ids = FollowedUser.objects.filter(user=user).values_list('followed_by_id', flat=True)
        users = User.objects.filter(id__in=following_ids)
        return users

class FollowCreateDeleteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request, user_id, following):
        if request.user.id != user_id:
            return Response(status=HTTPStatus.FORBIDDEN)

        if not User.objects.filter(id=user_id).exists() or not User.objects.filter(id=following).exists():
            return Response(status=HTTPStatus.NOT_FOUND)
        if FollowedUser.objects.filter(user_id=following, followed_by_id=user_id).exists():
            return Response(status=HTTPStatus.CONFLICT)

        follow = FollowedUser.objects.create(user_id=following, followed_by_id=user_id)
        follow.save()
        follow_user = self.get_serializer(User.objects.get(id=user_id)) # request.user
        followed_user = self.get_serializer(User.objects.get(id=following))
        data = {
            "user": follow_user.data,
            "following": followed_user.data
        }
        return Response(data, status=HTTPStatus.CREATED)

    def delete(self, request, user_id, following):
        if request.user.id != user_id:
            return Response(status=HTTPStatus.FORBIDDEN)

        if not User.objects.filter(id=user_id).exists() or not User.objects.filter(id=following).exists():
            return Response(status=HTTPStatus.NOT_FOUND)
        if not FollowedUser.objects.filter(user_id=following, followed_by_id=user_id).exists():
            return Response(status=HTTPStatus.CONFLICT)

        follow = FollowedUser.objects.get(user_id=following, followed_by_id=user_id)
        follow.delete()

        return Response(status=HTTPStatus.OK)

class SavedPostListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = SimplePagination

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        post_ids = SavedPost.objects.filter(user=user).values_list('post_id', flat=True)
        posts = Post.objects.filter(id__in=post_ids)
        return posts

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user_id = self.kwargs['user_id']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=HTTPStatus.NOT_FOUND)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(user=user, instance=queryset, many=True)
        return Response(serializer.data)

class SavedPostCreateDeleteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def post(self, request, user_id, feed_id):
        if not User.objects.filter(id=user_id).exists() or not Post.objects.filter(id=feed_id).exists():
            return Response(status=HTTPStatus.NOT_FOUND)
        if SavedPost.objects.filter(user_id=user_id, post_id=feed_id).exists():
            return Response(status=HTTPStatus.CONFLICT)

        saved_post = SavedPost.objects.create(user_id=user_id, post_id=feed_id)
        saved_post.save()
        user = saved_post.user
        post = saved_post.post
        self.serializer_class = PostSerializer
        serializer = self.get_serializer(instance=post)
        return Response(serializer.data, status=HTTPStatus.CREATED)

    def delete(self, request, user_id, feed_id):
        if not User.objects.filter(id=user_id).exists() or not Post.objects.filter(id=feed_id).exists():
            return Response(status=HTTPStatus.NOT_FOUND)
        if not SavedPost.objects.filter(user_id=user_id, post_id=feed_id).exists():
            return Response(status=HTTPStatus.CONFLICT)

        saved_post = SavedPost.objects.get(user_id=user_id, post_id=feed_id)
        saved_post.delete()

        return Response(status=HTTPStatus.OK)
