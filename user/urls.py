from django.urls import path

from . import views

urlpatterns = [
    path('user', views.UserSignupSearchView.as_view()),
    path('user/<str:user_id>', views.UserDetailUpdateDeleteView.as_view()),
    path('user/<str:user_id>/following', views.FollowingListView.as_view()),
    path('user/<str:user_id>/following/<str:following>', views.FollowCreateDeleteView.as_view()),
    path('user/<str:user_id>/follower', views.FollowerListView.as_view()),
    # path('user/<str:user_id>/saved', views.SavedPostListView.as_view()),
    # path('user/<str:user_id>/saved/<str:feed_id>', views.SavedPostCreateDeleteView.as_view()),
]
