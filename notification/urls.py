from django.urls import path

from . import views

urlpatterns = [
    path('notification', views.NotificationListView.as_view())
]
