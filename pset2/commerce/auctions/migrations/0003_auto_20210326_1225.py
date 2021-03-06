# Generated by Django 3.1.7 on 2021-03-26 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20210325_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('a', 'Other'), ('b', 'Electronics'), ('c', 'Home'), ('d', 'Sports'), ('e', 'Toys'), ('f', 'Clothes')], default='Other', max_length=1),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.URLField(blank=True),
        ),
    ]
