# Generated by Django 3.1.7 on 2021-04-28 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20210428_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='status',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('closed', 'Closed')], default='active', max_length=10),
        ),
    ]
