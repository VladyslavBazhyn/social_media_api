# Generated by Django 5.0.7 on 2024-08-22 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_media_user', '0005_alter_user_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
    ]
