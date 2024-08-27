from datetime import datetime

from celery import shared_task

from django.contrib.auth import get_user_model

from django.utils import timezone

from social_media_base.models import Post


@shared_task
def planning_post_creation(
    user_id: int,
    when: datetime,
    post_text: str = "Just a new post",
    hashtags: str = "#automatic",
):

    # Find correct user who create this schedule
    User = get_user_model()
    user = User.objects.get(id=user_id)

    # Creating a post only when time is appropriate
    if timezone.now() >= when:
        post = Post.objects.create(
            owner=user,
            text=post_text,
            hashtags=hashtags
        )
        return f"Post created with ID {post.id}"

    else:
        planning_post_creation.apply_async((user_id, when, post_text, hashtags), eta=when)
        return f"Task rescheduled for {when}"
