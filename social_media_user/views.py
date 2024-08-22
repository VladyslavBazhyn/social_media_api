from django.contrib.auth import get_user_model
from drf_spectacular.types import OpenApiTypes
from rest_framework import generics, viewsets, permissions

from drf_spectacular.utils import extend_schema, OpenApiParameter

from social_media_api.permissions import IsOwnerOrReadOnly, IsUserItself
from social_media_user.serializers import (
    UserCreateSerializer,
    UserManageSerializer,
    UserListSerializer,
    UserDetailSerializer, UserChangePasswordSerializer
)


class CreateUserViewSet(generics.CreateAPIView):
    """
    View set for new users to create an account
    """
    serializer_class = UserCreateSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.AllowAny]  # Everyone need to be able to create new account
    authentication_classes = []  # Nothing authentication here, everyone need to be able to create new account


class ChangePasswordView(generics.UpdateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = [IsUserItself]
    serializer_class = UserChangePasswordSerializer


class ManageUserViewSet(generics.RetrieveUpdateDestroyAPIView):
    """
    View set for regular user which allow them
    to make all manipulation with their own account
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserManageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    """View set for retrieving different data about user by other users"""

    queryset = get_user_model().objects.all()

    def get_serializer_class(self):
        """
        Get correct serializer correspondingly
        to provided request type
        """

        if self.action == "retrieve":
            return UserDetailSerializer
        return UserListSerializer

    def get_queryset(self):
        """
        Get correct queryset with provided filtering
        """
        queryset = self.queryset

        nickname = self.request.data.get("nickname", None)

        if nickname:
            queryset = queryset.filter(nickname__icontains=nickname)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="nickname",
                description="Filter by user's nickname (ex. ?nickname=smith)",
                required=False,
                type=OpenApiTypes.STR
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
