# Generated by Django 5.0.7 on 2024-08-23 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social_media_user", "0008_blacklistedaccesstoken"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blacklistedaccesstoken",
            name="token",
            field=models.TextField(max_length=500),
        ),
    ]
