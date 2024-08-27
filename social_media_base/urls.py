"""All URLs for all models of social media API except user's urls"""

from django.urls import path, include
from rest_framework import routers

from social_media_base.views import PostViewSet, ScheduledPostCreationView
from social_media_user.views import UserViewSet, follow, unfollow

app_name = "base"

router = routers.DefaultRouter()

router.register("users", UserViewSet)
router.register("posts", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("users/<int:pk>/follow/", follow, name="follow_user"),
    path("users/<int:pk>/unfollow/", unfollow, name="unfollow_user"),
    path("posts/schedule_post", ScheduledPostCreationView.as_view(), name="post_schedule")
]
