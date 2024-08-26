"""All basic models like post and comment here"""
from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    text = models.TextField()
    post_image = models.ImageField(null=True, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    hashtags = models.TextField(max_length=100, null=True, blank=True)
