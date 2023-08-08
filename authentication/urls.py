from django.urls import path

from . import views

urlpatterns = [
    path('auth/token', views.mock.auth_token),
    path('auth/validation', views.mock.auth_validation),
    path('auth/validation/check', views.mock.auth_validation_check),
    path('auth/reset-password', views.mock.auth_reset_password),
]
