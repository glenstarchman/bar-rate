# Generated by Django 2.2.2 on 2019-06-04 00:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_auto_20190604_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barmeta',
            name='atmosphere',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Atmosphere'),
        ),
    ]
