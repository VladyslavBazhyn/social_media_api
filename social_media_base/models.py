"""All basic models like post and comment here"""

from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    """Base post model"""

    text = models.TextField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    hashtags = models.TextField(max_length=100, null=True, blank=True)
