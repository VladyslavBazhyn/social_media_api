# Generated by Django 5.0.7 on 2024-08-22 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social_media_user", "0004_alter_user_first_name_alter_user_last_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="nickname",
            field=models.TextField(blank=True, unique=True),
        ),
    ]
