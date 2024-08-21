from rest_framework import viewsets

from social_media_api.permissions import IsOwnerOrReadOnly
from social_media_base.models import Post
from social_media_base.serializers import PostBaseSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostBaseSerializer
    queryset = Post.objects.all()

    def get_permissions(self):

        permission_classes = self.permission_classes

        if self.request.method == "POST":
            permission_classes = [IsOwnerOrReadOnly]

        return [permission() for permission in permission_classes]
