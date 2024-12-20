"""All URLs for user model"""

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from social_media_user.views import (
    ManageUserViewSet,
    CreateUserViewSet,
    ChangePasswordView,
    UserLogoutView,
    UserLogoutAllView,
)

app_name = "user"


urlpatterns = [
    path("me/", ManageUserViewSet.as_view(), name="manage"),
    path("register/", CreateUserViewSet.as_view(), name="register"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("logout_all/", UserLogoutAllView.as_view(), name="logout_all"),
    path(
        "change_password/<int:pk>/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
