# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-01 20:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_baralsoknownas_closed_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='barmeta',
            name='non_alchohol_friendly',
            field=models.BooleanField(default=True),
        ),
    ]
