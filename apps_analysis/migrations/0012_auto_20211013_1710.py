# Generated by Django 2.2 on 2021-10-13 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_analysis', '0011_auto_20211013_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_analysis',
            name='os_version',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
    ]