from django.urls import path
from .views import PostNew, CommentNew, PostLike, CommentLike

urlpatterns = [
    path('new/', PostNew.as_view(), name="post"),
    path('comment/new/', CommentNew.as_view(), name="comment"),
    path('post/like/<slug:slug>/', PostLike.as_view(), name="like_post"),
    path('comment/like/<slug:slug>/', CommentLike.as_view(), name="like_comment"),
]
