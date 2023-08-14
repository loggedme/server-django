from http import HTTPStatus
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.db.models import Q
from django.db.models import Count

from .models import User, FollowedUser
# from badge.models import Badge, BadgedUser
from feed.models import Post, SavedPost
from .serializers import UserSerializer
# from badge.serializers import BadgeSerializer
from feed.serializers import PostSerializer
from feed.pagination import SimplePagination

from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination

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
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=HTTPStatus.NOT_FOUND)

    def get(self, request, user_id):
        user = self.get_object(user_id)
        serializer = UserSerializer(user)
        data = {
            "user": serializer.data,
            # "badge": {"items": BadgeSerializer(badge, many=True).data}
        }
        return Response(data, status=HTTPStatus.OK)

    def patch(self, request, user_id):
        user = self.get_object(user_id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

    def delete(self, request, user_id):
        self.permission_classes = [permissions.IsAuthenticated]
        user = self.get_object(user_id)
        user.is_active = False
        user.save()
        return Response(status=HTTPStatus.OK)
        
class UserSignupSearchView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    pagination_class = UserPagenation
    
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        type = self.request.query_params.get('type')
        query = self.request.query_params.get('query')
        recommend = self.request.query_params.get('recommend')
        
        if recommend:   # 태그 추천
            if type == "business":
                users = User.objects.annotate(
                    follower_count=Count('followed_user', distinct=True)
                    ).filter(account_type=2).order_by('-follower_count')[:5]
            elif type == "personal":
                users = User.objects.annotate(
                    follower_count=Count('followed_user', distinct=True)
                    ).filter(account_type=1).order_by('-follower_count')[:5]
            elif not type:
                users = User.objects.annotate(
                    follower_count=Count('followed_user', distinct=True)
                    ).order_by('-follower_count')[:5]
        elif type and query:  # 검색
            if type == "business":
                users = User.objects.filter(Q(name__icontains=query) | Q(handle__icontains=query), account_type=2)
            elif type == "personal":
                users = User.objects.filter(Q(name__icontains=query) | Q(handle__icontains=query), account_type=1)
        else:
            return Response(status=HTTPStatus.BAD_REQUEST)
        
        return users
        
class FollowingListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = UserPagenation
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        following_ids = FollowedUser.objects.filter(followed_by_id=user_id).values_list('user_id', flat=True)
        users = User.objects.filter(id__in=following_ids)
        return users
    
class FollowerListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = UserPagenation
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        following_ids = FollowedUser.objects.filter(user_id=user_id).values_list('followed_by', flat=True)
        users = User.objects.filter(id__in=following_ids)
        return users

class FollowCreateDeleteView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, user_id, following):
        if not User.objects.filter(id=user_id).exists() or not User.objects.filter(id=user_id).exists():
            return Response(status=HTTPStatus.NOT_FOUND)
        if FollowedUser.objects.filter(user_id=following, followed_by_id=user_id).exists():
            return Response(status=HTTPStatus.CONFLICT)
        
        follow = FollowedUser.objects.create(user_id=following, followed_by_id=user_id)
        follow.save()
        follow_user = UserSerializer(User.objects.get(id=user_id)) # request.user
        followed_user = UserSerializer(User.objects.get(id=following))
        data = {
            "user": follow_user.data,
            "following": followed_user.data
        }
        return Response(data, status=HTTPStatus.CREATED)
    
    def delete(self, request, user_id, following):
        if not User.objects.filter(id=user_id).exists() or not User.objects.filter(id=user_id).exists():
            return Response(status=HTTPStatus.NOT_FOUND)
        if not FollowedUser.objects.filter(user_id=following, followed_by_id=user_id).exists():
            return Response(status=HTTPStatus.CONFLICT)
        
        follow = FollowedUser.objects.get(user_id=following, followed_by_id=user_id)
        follow.delete()
        
        return Response(status=HTTPStatus.OK)

class SavedPostListView(generics.ListAPIView):
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
        user = User.objects.get(id=user_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(user=user, instance=page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(user=user, instance=queryset, many=True)
        return Response(serializer.data)

class SavedPostCreateDeleteView(generics.GenericAPIView):
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
        serializer = PostSerializer(user=user, instance=post)
        return Response(serializer.data, status=HTTPStatus.CREATED)
    
    def delete(self, request, user_id, feed_id):
        if not User.objects.filter(id=user_id).exists() or not Post.objects.filter(id=feed_id).exists():
            return Response(status=HTTPStatus.NOT_FOUND)
        if not SavedPost.objects.filter(user_id=user_id, post_id=feed_id).exists():
            return Response(status=HTTPStatus.CONFLICT)
        
        saved_post = SavedPost.objects.get(user_id=user_id, post_id=feed_id)
        saved_post.delete()
        
        return Response(status=HTTPStatus.OK)
