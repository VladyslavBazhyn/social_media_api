# Generated by Django 5.0.7 on 2024-08-25 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social_media_base", "0004_alter_post_like"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="hashtags",
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]