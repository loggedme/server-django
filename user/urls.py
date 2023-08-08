from django.urls import path

from . import views

urlpatterns = [
    path('user', views.user_detail_or_search),
    path('user/<str:user_id>', views.UserApi.as_view()),
    path('user/<str:user_id>/following', views.FollowApi.as_view()),
    path('user/<str:user_id>/following/<str:following>', views.FollowApi.as_view()),
    path('user/<str:user_id>/follower', views.follower_list_api),
    path('/user/<str:user_id/saved', views.SavedPostApi.as_view()),
    path('/user/<str:user_id/saved/<str:feed_id>', views.SavedPostApi.as_view()),
]
