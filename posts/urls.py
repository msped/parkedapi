from django.urls import path
from .views import PostNew

urlpatterns = [
    path('post/new/', PostNew.as_view(), name="post"),
]
