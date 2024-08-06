"""All URLs for user model"""


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from social_media_user.views import ManageUserViewSet, UserViewSet

app_name = "user"

router = routers.DefaultRouter()

router.register("users", UserViewSet)

urlpatterns = [
    path("me/", ManageUserViewSet.as_view(), name="manage"),
    path("", include(router.urls))
    # path("users/<int: pk>", UserViewSet.as_view(), name="users-detail")  # Need to chck how to write it properly
]
