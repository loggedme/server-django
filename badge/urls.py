from django.urls import path

from . import views

urlpatterns = [
    path('badge', views.BadgeApi.as_view()),
    path('badge/<str:badge_id>', views.BadgeApi.as_view()),
    path('user/<str:user_id>/badge', views.UserBadgeApi.as_view()),
    path('user/<str:user_id>/badge/<str:badge_id>', views.UserBadgeApi.as_view()),
]
