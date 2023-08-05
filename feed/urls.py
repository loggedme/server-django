from django.urls import path

from . import views

urlpatterns = [
    path('feed', views.mock.post),
    path('feed/<str:post_id>', views.mock.post_id),
    path('feed/<str:post_id>/like', views.mock.post_id_like),
    path('feed/<str:post_id>/comment', views.mock.post_id_comment),
    path('feed/<str:post_id>/comment/<str:comment_id>', views.mock.post_id_comment_id),
]
