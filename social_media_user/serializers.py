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
        validated_data.pop("password2", None)
        validated_data.pop("old_password", None)

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def validate(self, attrs):
        """Function to validate whether two wrote passwords are same"""
        if (
            (attrs.get("password") and attrs.get("password2"))
            and (attrs["password"] != attrs["password2"])
        ):
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        """Function to validate whether old password wrote correctly"""
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def validate_email(self, value):
        user = self.context["request"].user
        if get_user_model().objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_nickname(self, value):
        user = self.context["request"].user
        if get_user_model().objects.exclude(pk=user.pk).filter(nickname=value).exists():
            raise serializers.ValidationError({"nickname": "This nickname is already in use."})
        return value


class UserCreateSerializer(UserBaseSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "nickname",
            "password",
            "password2"
        ]
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5},
            "password2": {"write_only": True, "min_length": 5}
        }


class UserChangePasswordSerializer(UserBaseSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ["old_password", "password", "password2"]


class UserManageSerializer(UserBaseSerializer):
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)

    class Meta:
        model = get_user_model()
        fields = [
            "nickname",
            "first_name",
            "last_name",
            "bio",
            "birth_date",
            "image",
            "my_subscriptions",
        ]


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
