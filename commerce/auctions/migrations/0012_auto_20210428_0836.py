# Generated by Django 3.1.7 on 2021-04-28 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20210423_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='slug',
            field=models.SlugField(default='item_name', max_length=250, unique_for_date='posting_date'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='status',
            field=models.IntegerField(blank=True, choices=[('active', 'Active'), ('closed', 'Closed')], default='active'),
        ),
    ]
