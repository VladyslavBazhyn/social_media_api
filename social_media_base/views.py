from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, response, status
from rest_framework.decorators import action

from social_media_api.permissions import IsOwnerOrReadOnly
from social_media_base.models import Post
from social_media_base.serializers import PostListSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostListSerializer

    def get_permissions(self):

        permission_classes = self.permission_classes

        if self.request.method == "POST":
            permission_classes = [IsOwnerOrReadOnly]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
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
                type=OpenApiTypes.STR
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
