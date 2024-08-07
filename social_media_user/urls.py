"""All URLs for user model"""


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from social_media_user.views import ManageUserViewSet, UserViewSet

app_name = "user"

router = routers.DefaultRouter()

router.register("users", UserViewSet)

urlpatterns = [
    path("me/", ManageUserViewSet.as_view(), name="manage"),
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
