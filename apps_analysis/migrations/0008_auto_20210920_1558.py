# Generated by Django 2.2 on 2021-09-20 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_analysis', '0007_subscriptionmethod_subscriptionplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionmethod',
            name='date',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='subscriptionplan',
            name='date',
            field=models.TextField(default='', max_length=500),
        ),
    ]
