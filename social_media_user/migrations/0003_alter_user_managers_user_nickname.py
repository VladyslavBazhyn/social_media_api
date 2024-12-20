# Generated by Django 5.0.7 on 2024-08-05 14:13

import social_media_user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social_media_user", "0002_user_bio_user_birth_date_user_image_and_more"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", social_media_user.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="nickname",
            field=models.TextField(blank=True),
        ),
    ]
