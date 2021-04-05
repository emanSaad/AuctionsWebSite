# Generated by Django 3.1.7 on 2021-04-05 17:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210405_1710'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auction',
            options={'ordering': ['posting_date']},
        ),
        migrations.AlterField(
            model_name='auction',
            name='close_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='auction',
            name='posting_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]