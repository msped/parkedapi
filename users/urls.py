from django.urls import path, include

from .views import (
    BlacklistTokenView,
    ChangePasswordView,
    FollowView,
    GetFollowingView,
    GetFollowersView,
    BlockView,
)

urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.urls')),
    path('jwt/blacklist/', BlacklistTokenView.as_view(), name="logout"),
    path(
        'change-password/',
        ChangePasswordView.as_view(),
        name="change_password"
    ),
    path('follow/<str:username>/', FollowView.as_view(), name="follow"),
    path('following/<str:username>/', GetFollowingView.as_view(), name="get_following"),
    path('followers/<str:username>/', GetFollowersView.as_view(), name="get_followers"),
    path('block/<str:username>/', BlockView.as_view(), name="block_user"),
]
