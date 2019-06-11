# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-01 17:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190601_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeGroup',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'age_group',
            },
        ),
        migrations.CreateModel(
            name='Atmosphere',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'atmosphere',
            },
        ),
        migrations.CreateModel(
            name='BarCheckin',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('comment', models.CharField(max_length=512)),
                ('public', models.BooleanField(default=True)),
                ('bar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Bar')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'bar_checkin',
            },
        ),
        migrations.RemoveField(
            model_name='barmeta',
            name='allows_kids',
        ),
        migrations.RemoveField(
            model_name='barmeta',
            name='has_food',
        ),
        migrations.RemoveField(
            model_name='barmeta',
            name='has_music',
        ),
        migrations.RemoveField(
            model_name='barmeta',
            name='has_patio',
        ),
        migrations.AddField(
            model_name='barmeta',
            name='atm',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='bar_stool_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='board_games',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='capacity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='chargers',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='draft_beer',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='food',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='jukebox',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='kids',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='live_music',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='patio',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='pool',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='pulltabs',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='schwag',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='shuffleboard',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='smoking_area',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='tables',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='tvs',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='unisex_bathroom',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='video_games',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='age_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.AgeGroup'),
        ),
        migrations.AddField(
            model_name='barmeta',
            name='atmosphere',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Atmosphere'),
        ),
    ]
