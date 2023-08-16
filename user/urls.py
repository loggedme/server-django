from django.urls import path

from . import views

urlpatterns = [
    path('user', views.UserSignupSearchView.as_view()),
    path('user/<uuid:user_id>', views.UserDetailUpdateDeleteView.as_view()),
    path('user/<uuid:user_id>/following', views.FollowingListView.as_view()),
    path('user/<uuid:user_id>/following/<uuid:following>', views.FollowCreateDeleteView.as_view()),
    path('user/<uuid:user_id>/follower', views.FollowerListView.as_view()),
    path('user/<uuid:user_id>/saved', views.SavedPostListView.as_view()),
    path('user/<uuid:user_id>/saved/<uuid:feed_id>', views.SavedPostCreateDeleteView.as_view()),
]
