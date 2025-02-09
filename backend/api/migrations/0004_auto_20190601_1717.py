# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-01 17:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190601_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='BarPopularHours',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('bar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Bar')),
            ],
            options={
                'db_table': 'bar_popular_hours',
            },
        ),
        migrations.AddField(
            model_name='barmeta',
            name='popular_hours',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.BarPopularHours'),
        ),
    ]
