"""All basic models like post and comment here"""
from django.contrib.auth import get_user_model
from django.db import models


class Post(models.Model):
    text = models.TextField()
    post_image = models.ImageField(null=True, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    like_unlike = models.BooleanField(blank=True, default=None)  # Am I need to create some sastome method in viewset to switch this parameter?
    comment = models.CharField(max_length=155, null=True, blank=True, )
