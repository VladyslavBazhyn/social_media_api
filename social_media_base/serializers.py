from rest_framework import serializers

from social_media_base.models import Post


class PostBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "post_image",
            "text",
            "owner",
            "like_unlike",
            "comment"
        ]
