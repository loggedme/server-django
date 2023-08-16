from django.urls import path

from . import views

urlpatterns = [
    path('badge', views.BadgeCreateView.as_view()),
    path('badge/<uuid:badge_id>', views.BadgeUpdateDeleteView.as_view()),
    path('badge/<uuid:badge_id>/user', views.BadgedUserCreateDeleteView.as_view()),
]
