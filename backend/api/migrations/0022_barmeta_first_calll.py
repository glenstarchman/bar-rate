# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-02 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_barmeta_wifi'),
    ]

    operations = [
        migrations.AddField(
            model_name='barmeta',
            name='first_calll',
            field=models.BooleanField(default=False),
        ),
    ]
