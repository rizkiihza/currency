# Generated by Django 2.1.7 on 2019-02-16 04:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency_processor', '0013_auto_20190215_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='date',
            field=models.DateField(default=datetime.date(2019, 2, 16)),
        ),
    ]
