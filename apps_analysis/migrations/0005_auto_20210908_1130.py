# Generated by Django 2.2 on 2021-09-08 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_analysis', '0004_auto_20210908_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adword_data',
            name='spends',
            field=models.FloatField(default=0),
        ),
    ]
