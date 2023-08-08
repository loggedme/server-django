from django.urls import path

from . import views

urlpatterns = [
    path('badge', views.BadgeApi.as_view()),
    path('badge/<str:badge_id>', views.BadgeApi.as_view()),
    path('/user/<str:user.id>/badge', views.UserBadgeApi.as_view()),
    path('/user/<str:user.id>/badge/<str:badge.id>', views.UserBadgeApi.as_view()),
]
