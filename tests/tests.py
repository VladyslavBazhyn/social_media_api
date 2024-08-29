"""Tests for social_media_api project"""
from django.contrib.auth import get_user_model
from django.test import TestCase

from unittest.mock import patch

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APIRequestFactory

from social_media_base.models import Post
from social_media_base.serializers import PostListSerializer, PostDetailSerializer, ScheduledPostSerializer
from social_media_user.serializers import UserListSerializer, UserDetailSerializer, UserCreateSerializer
from tests.sample_functions import sample_post, sample_user

POST_URL = reverse("base:post-list")
USER_URL = reverse("base:user-list")
USER_REGISTER_URL = reverse("user:register")
POST_SCHEDULE_URL = reverse("base:post_schedule")


def get_post_detail_url(post_id: int) -> str:
    """Return URL for detail endpoint of given id"""
    return reverse(
        "base:post-detail",
        args=[post_id]
    )


def get_user_detail_url(user_id: int) -> str:
    """Return URL for detail endpoint of given id"""
    return reverse(
        "base:user-detail",
        args=[user_id]
    )


class UnAuthenticatedUserSocialMediaApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """
        Test whether unauthenticated user can't get access to closed endpoints
        but can register.
        """
        res = self.client.get(POST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        res = self.client.get(POST_SCHEDULE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        res = self.client.post(
            USER_REGISTER_URL,
            {
                "email": "sample@sample.com",
                "password": "samplepassword",
                "password2": "samplepassword"
            },
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class AuthenticatedUserSocialMediaApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
            password2="testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_post_retrieve_correct_serializer(self):
        """
        Test whether different post endpoints retrieve correct serializers
        """
        sample_post(
            user_id=self.user.pk,
            post_text="Serializer test post 1",
            post_hashtags="#First"
        )
        sample_post(
            user_id=self.user.pk,
            post_text="Serializer test post 2",
            post_hashtags="#Second"
        )
        sample_post(
            user_id=self.user.pk,
            post_text="Serializer test post 3",
            post_hashtags="#Therd"
        )

        #  Check list serializer
        res = self.client.get(
            POST_URL
        )
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

        # Check detail serializer
        res = self.client.get(
            get_post_detail_url(1)
        )
        post = Post.objects.get(id=1)
        serializer = PostDetailSerializer(post)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

        # Check post schedule
        res = self.client.post(
            POST_SCHEDULE_URL,
            {
                "when": "2025-01-01T00:00",
                "post_text": "Some text",
                "hashtags": "#test"
            },
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_retrieve_correct_serializer(self):
        # Get all users
        users = get_user_model().objects.all()
        serializer = UserListSerializer(users, many=True)
        # Go on users list endpoint
        res = self.client.get(
            USER_URL
        )
        # Find correspondence
        self.assertEqual(res.data, serializer.data)

        # Get especial user
        user = get_user_model().objects.filter(id=self.user.pk).first()
        serializer = UserDetailSerializer(user)
        # Go on user detail endpoint
        res = self.client.get(
            get_user_detail_url(user_id=user.id)
        )
        # Find correspondence
        self.assertEqual(res.data, serializer.data)

    def test_user_create_serializer_working_correct(self):

        # Check whether create serializer working correctly in correct data
        user_data = {
            "email": "sample@sample.com",
            "password": "sample",
            "password2": "sample"
        }
        serializer = UserCreateSerializer(data=user_data)
        self.assertTrue(serializer.is_valid())

        # Check whether create serializer return error when not all data exist
        user_data = {
            "email": "sample@sample.com",
            "password": "sample",
        }
        serializer = UserCreateSerializer(data=user_data)
        self.assertFalse(serializer.is_valid())

        # Check whether create serializer return error when email not unique
        user_data = {
            "email": "test@test.com",
            "password": "sample",
            "password2": "sample"
        }
        serializer = UserCreateSerializer(data=user_data)
        self.assertFalse(serializer.is_valid())

        # Check whether create serializer return error when passwords not same
        user_data = {
            "email": "test@test.com",
            "password": "sample",
            "password2": "sampleeee"
        }
        serializer = UserCreateSerializer(data=user_data)
        self.assertFalse(serializer.is_valid())

    def test_post_and_user_filtering(self):
        """
        Test of filtering post and user lists
        """
        #  Create some users
        user_1 = sample_user(
            "first@first.com", "firstpass", "firstpass"
        )
        user_1.nickname = "user_1"

        user_2 = sample_user(
            "second@second.com", "secondpass", "secondpass"
        )
        user_2.nickname = "user_2"

        user_3 = sample_user(
            "therd@therd.com", "therdpass", "therdpass"
        )
        user_3.nickname = "therd"

        # Create some posts
        sample_post(user_id=self.user.pk)
        sample_post(user_id=self.user.pk)
        sample_post(user_id=self.user.pk, post_hashtags="#therd")

        # Filtering by nickname__icontains 'user'
        users = get_user_model().objects.filter(nickname="user")
        users_serializer = UserListSerializer(users, many=True)

        # Filtering by post's hashtag
        posts = Post.objects.filter(hashtags="#therd")
        posts_serializer = PostListSerializer(posts, many=True)

        # Whether filtering correct
        res = self.client.get(
            POST_URL,
            {"hashtag": "ther"}
        )
        self.assertEqual(res.data, posts_serializer.data)

        # Whether filtering correct
        res = self.client.get(
            USER_URL,
            {"nickname": "user"}
        )
        self.assertEqual(res.data, users_serializer.data)
