# Generated by Django 2.2.2 on 2019-06-12 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_auto_20190612_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='favorite_bars',
            field=models.ManyToManyField(related_name='favorite_bars', to='api.Bar'),
        ),
        migrations.AddField(
            model_name='profile',
            name='favorite_bartenders',
            field=models.ManyToManyField(related_name='favorite_bartenders', to='api.Bartender'),
        ),
    ]
