# Generated by Django 5.0.7 on 2024-08-25 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("social_media_base", "0002_rename_user_post_owner"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="like_unlike",
            new_name="like",
        ),
    ]