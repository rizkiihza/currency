# Generated by Django 2.1.7 on 2019-02-14 03:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currency_processor', '0009_auto_20190214_0354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rate',
            old_name='currency_form',
            new_name='currency_from',
        ),
    ]
