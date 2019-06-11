# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-01 17:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20190601_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barwith',
            name='mood',
        ),
        migrations.AddField(
            model_name='barcheckin',
            name='mood',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Mood'),
        ),
    ]
