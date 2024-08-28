from datetime import datetime

from rest_framework import serializers

from social_media_base.models import Post


class PostBaseSerializer(serializers.ModelSerializer):
    """
    Base post serializer to handle all functions and logic
    which is used in all other serializers
    """

    class Meta:
        model = Post
        fields = ["id", "text", "owner", "like", "comment", "hashtags"]

    def create(self, validated_data):
        """
        Creation without choosing an owner.
        Owner - always authenticated user which create this post
        """
        validated_data.update({"owner": self.context["request"].user})
        return super().create(validated_data)


class PostListSerializer(PostBaseSerializer):
    """Serializer for list demonstration"""

    class Meta:
        model = Post
        fields = ["text", "owner", "hashtags"]
        read_only_fields = [
            "owner",
        ]


class PostDetailSerializer(PostBaseSerializer):
    """Serializer for detail demonstration"""

    class Meta:
        model = Post
        fields = ["text", "hashtags", "owner"]
        read_only_fields = ["owner"]


class ScheduledPostSerializer(PostBaseSerializer):
    """Serializer for creating posts in some schedule"""

    # Expected format: "YYYY-MM-DDTHH:MM"
    when = serializers.DateTimeField(required=False, default=None)

    post_text = serializers.CharField(required=False, default="Just a new post")

    hashtags = serializers.CharField(required=False, default="#automatic")

    class Meta:
        model = Post
        fields = ["post_text", "hashtags", "when"]

    def validate_when(self, value):
        """Validation post creation time"""
        if value and value < datetime.now():
            raise serializers.ValidationError("Scheduled time cannot be in the past.")
        return value
