# Generated by Django 3.1.7 on 2021-06-07 22:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0016_auto_20210607_1540'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='followedUser',
        ),
        migrations.AddField(
            model_name='follow',
            name='followedUser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='followee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='follow',
            name='followingUser',
        ),
        migrations.AddField(
            model_name='follow',
            name='followingUser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]
