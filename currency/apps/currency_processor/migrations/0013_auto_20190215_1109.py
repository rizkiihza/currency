# Generated by Django 2.1.7 on 2019-02-15 11:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency_processor', '0012_auto_20190214_0700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='date',
            field=models.DateField(default=datetime.date(2019, 2, 15)),
        ),
    ]