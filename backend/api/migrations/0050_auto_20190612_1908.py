# Generated by Django 2.2.2 on 2019-06-12 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0049_delete_barreview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmark',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='bookmark',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='dislike',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='dislike',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='follower',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='follower',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='image',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='image',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='like',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='like',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='review',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='review',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='deleted',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='deleted_at',
        ),
    ]
