# Generated by Django 3.1.7 on 2021-04-14 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210413_1431'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='number_of_bids',
        ),
    ]
