from django.urls import path, include

from .views import (
    BlacklistTokenView,
    ChangePasswordView,
    FollowView,
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
    path('follow/<str:username>/', FollowView.as_view(), name="follow")
]
