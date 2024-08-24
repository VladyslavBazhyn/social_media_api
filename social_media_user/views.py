from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import generics, viewsets, permissions, views, response, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy

from rest_framework_simplejwt import tokens
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from social_media_api import authentication
from social_media_api.permissions import IsUserItself
from social_media_user.models import BlacklistedAccessToken
from social_media_user.serializers import (
    UserCreateSerializer,
    UserManageSerializer,
    UserListSerializer,
    UserDetailSerializer,
    UserChangePasswordSerializer
)


@login_required
def follow(request, pk):
    user_to_follow = get_object_or_404(get_user_model(), id=pk)
    if not request.user.following.filter(id=pk).exists():
        request.user.following.add(user_to_follow)
    return HttpResponseRedirect(reverse_lazy("base:user-detail", kwargs={"pk": pk}))


@login_required
def unfollow(request, pk):
    user_to_unfollow = get_object_or_404(get_user_model(), id=pk)
    if request.user.following.filter(id=pk).exists():
        request.user.following.remove(user_to_unfollow)
    return HttpResponseRedirect(reverse_lazy("base:user-detail", kwargs={"pk": pk}))


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


class UserLogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return response.Response({"error": "No refresh token provided."}, status=status.HTTP_400_BAD_REQUEST)

            token = tokens.RefreshToken(refresh_token)
            token.blacklist()

            access_token = request.headers.get("Authorization").split()[1]
            BlacklistedAccessToken.objects.create(
                token=access_token,
                user=request.user
            )

            return response.Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return response.Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAllView(views.APIView):
    permission_classes = [IsUserItself]

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return response.Response(status=status.HTTP_205_RESET_CONTENT)


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

        nickname = self.request.query_params.get("nickname", None)

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
