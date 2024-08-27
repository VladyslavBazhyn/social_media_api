from datetime import datetime

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


class ScheduledPostSerializer(PostBaseSerializer):
    when = serializers.DateTimeField(required=False, default=None)  # Expected format: "YYYY-MM-DDTHH:MM"
    post_text = serializers.CharField(required=False, default="Just a new post")
    hashtags = serializers.CharField(required=False, default="#automatic")

    class Meta:
        model = Post
        fields = [
            "post_text",
            "hashtags",
            "when"
        ]

    def validate_when(self, value):
        if value and value < datetime.now():
            raise serializers.ValidationError("Scheduled time cannot be in the past.")
        return value
