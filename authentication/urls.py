from django.urls import path

from . import views

urlpatterns = [
    path('auth/token', views.AuthTokenView.as_view()),
    path('auth/validation', views.AuthValidationView.as_view()),
    path('auth/validation/check', views.AuthValidationCheckView.as_view()),
    path('auth/reset-password', views.AuthResetPasswordView.as_view()),
]
