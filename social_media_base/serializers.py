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
            "like",
            "comment",
            "hashtags"
        ]

    def create(self, validated_data):
        validated_data.update(
            {"owner": self.context["request"].user}
        )
        return super().create(validated_data)


class PostListSerializer(PostBaseSerializer):
    class Meta:
        model = Post
        fields = [
            "post_image",
            "text",
            "owner",
            "hashtags"
        ]
        read_only_fields = [
            "owner",
        ]


class PostDetailSerializer(PostBaseSerializer):
    class Meta:
        model = Post
        fields = [
            "text",
            "post_image",
            "hashtags",
            "owner"
        ]
        read_only_fields = [
            "owner"
        ]
