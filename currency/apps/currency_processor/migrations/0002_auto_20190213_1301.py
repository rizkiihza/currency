# Generated by Django 2.1.7 on 2019-02-13 13:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('currency_processor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 2, 13, 13, 1, 17, 182161, tzinfo=utc)),
        ),
    ]
