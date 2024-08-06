"""All URLs for all models of social media API except user's urls"""


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from social_media_base.views import PostViewSet

app_name = "base"

router = routers.DefaultRouter()

router.register("posts", PostViewSet)

urlpatterns = [
    path("", include("social_media_user.urls", namespace="user")),
    path("", include(router.urls))
]
