# Generated by Django 2.2 on 2021-10-13 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_analysis', '0010_auto_20211013_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_analysis',
            name='app_version',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]