"""Sample functions for tests"""

from django.contrib.auth import get_user_model

from social_media_base.models import Post


def sample_post(
    user_id: int = None, post_text: str = "SAMPLE", post_hashtags: str = "#SAMPLE"
):
    owner = get_user_model().objects.get(id=user_id)
    post = Post.objects.create(owner=owner, text=post_text, hashtags=post_hashtags)
    return post


def sample_user(email: str, password: str, password2: str):
    return get_user_model().objects.create_user(
        email=email, password=password, password2=password2
    )
