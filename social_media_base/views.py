import datetime

from django.utils import timezone

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from social_media_api.permissions import IsOwnerOrReadOnly
from social_media_api.tasks import planning_post_creation
from social_media_base.models import Post
from social_media_base.serializers import (
    PostListSerializer,
    PostDetailSerializer,
    ScheduledPostSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    """Base view set for handling all posts basic needs"""

    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostListSerializer

    def get_permissions(self):
        """
        Choosing correct permission to get users option to delete their posts
        """
        permission_classes = self.permission_classes

        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            permission_classes = [IsOwnerOrReadOnly]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Get queryset with appropriate filter if user searching throw posts
        """
        queryset = self.queryset

        hashtag = self.request.query_params.get("hashtag", None)

        if hashtag:
            queryset = queryset.filter(hashtags__icontains=hashtag)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="hashtag",
                description="Filter by hashtags (ex. ?hashtag=morning)",
                required=False,
                type=OpenApiTypes.STR,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ScheduledPostCreationView(generics.CreateAPIView):
    """Special view for scheduling post creation"""

    queryset = Post.objects.all()
    serializer_class = ScheduledPostSerializer

    def post(self, request):

        user_id = request.user.id

        # Wrote data or standard values
        post_text = request.data.get("post_text", "Just a new post")
        hashtags = request.data.get("hashtags", "#authomatic")

        # This should be a str in "%Y-%m-%dT%H:%M" format
        when = request.data.get("when")
        # Convert it to a datetime.datetime format
        try:
            when = timezone.make_aware(
                datetime.datetime.strptime(when, "%Y-%m-%dT%H:%M")
            )
        except ValueError:
            return Response(
                {"message": "You need to write a time in appropriate format"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Trigger the Celery task
        planning_post_creation.apply_async(args=[user_id, when, post_text, hashtags])

        return Response({"message": "Post scheduled"}, status=status.HTTP_201_CREATED)
