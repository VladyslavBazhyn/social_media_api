""""User serializer here"""

from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "bio",
            "birth_date",
            "nickname",
            "image",
            "my_subscriptions",
            "is_stuff"
        )
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class UserCreateSerializer(UserBaseSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "password",
            "password2"
        ]
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5},
            "password2": {"write_only": True, "min_length": 5}
        }

    def validate(self, attrs):
        """VFunction to validate whether two wrote passwords are same"""
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs


class UserManageSerializer(UserBaseSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "nickname",
            "bio",
            "birth_date",
            "image",
            "my_subscriptions",
        ]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}


class UserListSerializer(UserBaseSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "nickname",
            "birth_date",
            "image",
        ]


class UserDetailSerializer(UserBaseSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "birth_date",
            "nickname",
            "image",
            "bio",
        ]
