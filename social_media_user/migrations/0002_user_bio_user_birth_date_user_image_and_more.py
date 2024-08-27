# Generated by Django 5.0.7 on 2024-08-02 13:10

import social_media_user.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social_media_user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="bio",
            field=models.TextField(default="Any biography here"),
        ),
        migrations.AddField(
            model_name="user",
            name="birth_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=social_media_user.models.user_image_file_path,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="my_subscriptions",
            field=models.ManyToManyField(
                related_name="my_followers", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
