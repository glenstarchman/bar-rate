# Generated by Django 2.2.2 on 2019-06-12 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0052_auto_20190612_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(default='USA', max_length=3),
        ),
    ]
