# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-03 16:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20190602_2159'),
    ]

    operations = [
        migrations.RunSQL("""
            ALTER TABLE gender DROP COLUMN IF EXISTS value
        """),
    ]
