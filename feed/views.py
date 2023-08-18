import json
from http import HTTPStatus
from uuid import UUID
from typing import List

from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework import generics
from rest_framework.exceptions import ValidationError, NotAuthenticated, PermissionDenied
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User, UserType
from user.services import get_user
from feed.pagination import simple_pagination, SimplePagination
from feed.models import *
from feed.serializers import *


class ToggleView(views.APIView):
    def get_queryset(self) -> QuerySet:
        pass

    def _set_attrs(self, request: HttpRequest, **kwargs):
        self.kwargs = kwargs
        self.request = request

    def post(self, request: HttpRequest, **kwargs):
        self._set_attrs(request, **kwargs)
        obj, created = self.get_queryset().get_or_create(**kwargs)
        return Response(status=status.HTTP_202_ACCEPTED if not created else status.HTTP_205_RESET_CONTENT)

    def delete(self, request: HttpRequest, **kwargs):
        self._set_attrs(request, **kwargs)
        obj, created = self.get_queryset().get_or_create(**kwargs)
        obj.delete()
        return Response(status=status.HTTP_202_ACCEPTED if created else status.HTTP_205_RESET_CONTENT)


class FeedListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    pagination_class = SimplePagination

    def get_queryset(self):
        queryset = Post.objects.order_by('-created_at')
        queryset = self._filter_queryset_type(queryset)
        queryset = self._filter_queryset_following(queryset)
        queryset = self._filter_queryset_trending(queryset)
        queryset = self._filter_queryset_hashtag(queryset)
        return queryset

    def _filter_queryset_type(self, queryset: QuerySet[Post]) -> QuerySet[Post]:
        raw_type = self.request.GET.get('type')
        if raw_type is None:
            return queryset
        for key, value in UserType.choices:
            if value.lower() == raw_type:
                return queryset.filter(created_by__account_type=key)
        raise ValidationError(f'"{raw_type}" is not a valid type. choices are ["personal", "business"]')

    def _filter_queryset_following(self, queryset: QuerySet[Post]) -> QuerySet[Post]:
        raw_following = self.request.GET.get('following')
        if raw_following is None:
            return queryset
        if raw_following == 'false':
            raise ValidationError('exclude followings is not supported.')
        if raw_following != '' and raw_following != 'true':
            raise ValidationError(f'"following={raw_following}" is invalid')
        if not self.request.user.is_authenticated:
            raise NotAuthenticated()
        user: User = self.request.user
        following_ids = user.following.values_list('user', flat=True)
        return queryset.filter(created_by__id__in=following_ids)

    def _filter_queryset_trending(self, queryset: QuerySet[Post]) -> QuerySet[Post]:
        if self.request.GET.get('trending', 'false') == 'false':
            return queryset
        return queryset.order_by('-likedpost')

    def _filter_queryset_hashtag(self, queryset: QuerySet[Post]) -> QuerySet[Post]:
        raw_hashtag = self.request.GET.get('hashtag')
        if raw_hashtag is None:
            return queryset
        if raw_hashtag != raw_hashtag.strip():
            raise ValidationError("spaces are not allowed for hashtag")
        if raw_hashtag == '':
            raise ValidationError("empty hashtag is not allowed")
        post_ids = HashTaggedPost.objects.filter(hashtag__name=raw_hashtag).values_list('post', flat=True)
        return queryset.filter(id__in=post_ids)


    def create(self, request: HttpRequest, *args, **kwargs):
        super().create
        user: User = request.user
        with transaction.atomic():
            if user.account_type == UserType.PERSONAL:
                post = self._create_personal_post(request)
            elif user.account_type == UserType.BUSINESS:
                post = self._create_business_post(request)
        return Response(data=self.get_serializer(instance=post).data, status=HTTPStatus.CREATED)

    def _create_personal_post(self, request: HttpRequest) -> Post:
            try:
                post = Post()
                post.content = request.data['content']
                post.tagged_user = get_user(request.data['tagged_user'])
                post.created_by = request.user
                post.save()
                self._create_post_images(request, post)
                return post
            except KeyError as e:
                raise ValidationError(str(e))

    def _create_business_post(self, request: HttpRequest) -> Post:
            try:
                post = Post()
                post.content = request.data['content']
                post.created_by = request.user
                post.save()
                self._create_post_images(request, post)
                return post
            except KeyError as e:
                raise ValidationError(str(e))

    def _create_post_images(self, request: HttpRequest, post: Post):
        images = request.FILES.getlist('images')
        if len(images) == 0 or len(images) > 10:
            raise ValidationError(f'{len(images)} images are not allowed.')
        for order, image in enumerate(images):
            postimage = PostImage()
            postimage.post = post
            postimage.image = image
            postimage.order = order
            postimage.save()


class FeedDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects


@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes([JWTAuthentication]) # 토큰을 사용한 로그인 검사 (외부모듈 사용)
class FeedDetailView(APIView):
    def get(self, request: HttpRequest, post_id: UUID, **kwargs):
        post = get_object_or_404(Post, id=post_id) # 피드 아이디에 해당하는 피드 가져옴
        serializer = PostSerializer(instance=post) # 로그인한 사용자 정보를 반영하여 피드 정보를 JSON으로 변경
        return Response(serializer.data, status=HTTPStatus.OK) # 재전송

    def put(self, request: HttpRequest, post_id: UUID, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        user: User = request.user
        data = json.loads(request.body)
        if post.created_by != user:
            return Response(status=HTTPStatus.FORBIDDEN)
        with transaction.atomic():
            post.content = data['content']
            if user.account_type == UserType.PERSONAL:
                try:
                    post.tagged_user = self.get_user_by_id_or_handle(data['tagged_user'])
                except User.DoesNotExist as e:
                    return Response(data={'tagged_user': e.args}, status=HTTPStatus.BAD_REQUEST)
            elif user.account_type == UserType.BUSINESS:
                post.tagged_user = None
            else:
                raise Exception()
            post.save()
            # TODO: 새로운 이미지 추가
            image_urls: List[str] = data['image_urls']
            for postimage in post.postimage_set.all():
                try:
                    postimage.order = image_urls.index(postimage.image.url)+1
                    postimage.save()
                except ValueError:
                    print(postimage.image.url, 'not found from', image_urls)
                    postimage.delete()
        if post.tagged_user is not None:
            notify_tag(notified_user=post.tagged_user, tagged_by=user, post=post)
        serializer = PostSerializer(instance=post)
        return Response(serializer.data, status=HTTPStatus.OK)

    def delete(self, request: HttpRequest, post_id: UUID, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        if post.created_by != request.user:
            return Response(status=HTTPStatus.FORBIDDEN)
        post.delete()
        return Response(status=HTTPStatus.OK)

    def get_user_by_id_or_handle(self, id_or_handle: str) -> User:
        kwargs = {}
        if self.is_uuid(id_or_handle):
            kwargs['id'] = UUID(id_or_handle)
        else:
            kwargs['handle'] = id_or_handle
        return User.objects.get(**kwargs)

    def is_uuid(self, uuid_to_test: str) -> bool:
        try:
            uuid_obj = UUID(uuid_to_test)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_to_test


class FeedLikeView(ToggleView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LikedPost.objects.filter(user=self.request.user)


class FeedSaveView(ToggleView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavedPost.objects.filter(user=self.request.user)


class CommentListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    pagination_class = SimplePagination
    queryset = Comment.objects

    def get_queryset(self):
        return super().get_queryset().filter(**self.kwargs)

    def perform_create(self, serializer):
        serializer.save(post_id=self.kwargs['post_id'])


class CommentDetailsView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    queryset = Comment.objects
    lookup_url_kwarg = 'comment_id'

    def perform_destroy(self, instance: Comment):
        if self.request.user != instance.created_by:
            raise PermissionDenied('자신이 작성한 댓글만 삭제할 수 있습니다.')
        return super().perform_destroy(instance)
