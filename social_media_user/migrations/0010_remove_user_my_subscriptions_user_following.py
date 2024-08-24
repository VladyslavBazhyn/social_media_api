# Generated by Django 5.0.7 on 2024-08-24 13:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_user', '0009_alter_blacklistedaccesstoken_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='my_subscriptions',
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]