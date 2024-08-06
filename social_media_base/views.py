from rest_framework import viewsets

from social_media_base.models import Post
from social_media_base.serializers import PostBaseSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostBaseSerializer
    queryset = Post.objects.all()
