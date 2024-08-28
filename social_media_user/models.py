"""User model which used in this project"""

import os
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext as _


def user_image_file_path(instance, filename):
    """Function for creation special unique filename for image"""
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/users/", filename)


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("Email must be sent")
        email = self.normalize_email(email)
        extra_fields.pop("password2", None)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    #  Credentials
    username = None
    email = models.EmailField(_("email address"), unique=True)

    #  User data itself
    bio = models.TextField(default="Any biography here")
    birth_date = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    # User's displaying for other users
    image = models.ImageField(upload_to=user_image_file_path, blank=True, null=True)
    nickname = models.TextField(blank=True, null=True, unique=True)

    #  User's preferences in social media
    following = models.ManyToManyField(
        "self", related_name="followers", symmetrical=False, blank=True
    )


class BlacklistedAccessToken(models.Model):
    token = models.TextField(max_length=500)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
