# Generated by Django 3.1.7 on 2021-05-28 22:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_post_likecount'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='follows',
            field=models.ManyToManyField(blank=True, related_name='_user_follows_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
