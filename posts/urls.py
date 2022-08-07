from django.urls import path
from .views import PostNew, CommentNew

urlpatterns = [
    path('post/new/', PostNew.as_view(), name="post"),
    path('comment/new/', CommentNew.as_view(), name="comment"),
]
