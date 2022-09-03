from django.urls import path

from .views import (CommentGetUpdateDestroy, CommentLike, CommentNew,
                    PostGetUpdateDestroy, PostLike, PostNew)

urlpatterns = [
    path('new/', PostNew.as_view(), name="new_post"),
    path('<slug:slug>/comment/new/', CommentNew.as_view(), name="new_comment"),
    path('like/<slug:slug>/', PostLike.as_view(), name="like_post"),
    path('comment/like/<int:comment_id>/', CommentLike.as_view(), name="like_comment"),
    path('<slug:slug>/', PostGetUpdateDestroy.as_view(), name="post"),
    path('comment/<int:comment_id>/', CommentGetUpdateDestroy.as_view(), name="comment"),
]
