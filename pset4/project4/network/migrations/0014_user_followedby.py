# Generated by Django 3.1.7 on 2021-06-04 20:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0013_auto_20210604_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followedby',
            field=models.ManyToManyField(blank=True, related_name='_user_followedby_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
