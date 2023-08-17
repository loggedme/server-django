from django.urls import path

from . import views

urlpatterns = [
    path('feed', views.FeedView.as_view()),
    path('feed/<uuid:post_id>', views.FeedDetailView.as_view()),
    path('feed/<uuid:post_id>/like', views.FeedLikeView.as_view()),
    path('feed/<uuid:post_id>/comment', views.FeedCommentView.as_view()),
    path('feed/<uuid:post_id>/comment/<uuid:comment_id>', views.FeedCommentDetailView.as_view()),
]
