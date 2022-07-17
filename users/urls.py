from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (
    RegisterView,
    BlacklistTokenView,
    ChangePasswordView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', BlacklistTokenView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path(
        'change-password/<int:profile_id>/',
        ChangePasswordView.as_view(),
        name="change_password"
    ),
]
