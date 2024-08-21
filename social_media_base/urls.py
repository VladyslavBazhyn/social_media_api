"""All URLs for all models of social media API except user's urls"""

from django.urls import path, include
from rest_framework import routers

from social_media_base.views import PostViewSet
from social_media_user.views import UserViewSet

app_name = "base"

router = routers.DefaultRouter()

router.register("users", UserViewSet)
router.register("posts", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
