from django.urls import path

from . import views

urlpatterns = [
    path('badge', views.BadgeApi.as_view()),
    path('badge/<str:badge_id>', views.BadgeApi.as_view()),
    path('badge/<str:badge_id>/user', views.BadgeUserApi.as_view()),
]
