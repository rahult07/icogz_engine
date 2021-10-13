# Generated by Django 2.2 on 2021-10-13 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_analysis', '0008_auto_20210920_1558'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Analysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_id', models.IntegerField(default=0)),
                ('app_launched_count', models.IntegerField(default=0)),
                ('uninstall_count', models.IntegerField(default=0)),
                ('app_launched_start_date', models.CharField(default='', max_length=500)),
                ('app_launched_end_date', models.CharField(default='', max_length=500)),
                ('uninstall_start_date', models.CharField(default='', max_length=500)),
                ('uninstall_end_date', models.CharField(default='', max_length=500)),
                ('install_count', models.IntegerField(default=0)),
                ('install_start_date', models.CharField(default='', max_length=500)),
                ('install_end_date', models.CharField(default='', max_length=500)),
                ('video_load_count', models.IntegerField(default=0)),
                ('video_load_start_date', models.CharField(default='', max_length=500)),
                ('video_load_end_date', models.CharField(default='', max_length=500)),
                ('video_progress_count', models.IntegerField(default=0)),
                ('video_progress_start_date', models.CharField(default='', max_length=500)),
                ('player_video_progress_end_date', models.CharField(default='', max_length=500)),
                ('os_version', models.FloatField(default=0)),
                ('app_version', models.IntegerField(default=0)),
                ('model_name', models.CharField(default='', max_length=500)),
                ('model', models.CharField(default='', max_length=500)),
                ('platform', models.CharField(default='', max_length=500)),
                ('ts', models.CharField(default='', max_length=500)),
                ('ct_app_version', models.FloatField(default=0)),
                ('ct_source', models.CharField(default='', max_length=500)),
                ('menu_click', models.IntegerField(default=0)),
                ('menu_start_date', models.CharField(default='', max_length=500)),
                ('menu_end_date', models.CharField(default='', max_length=500)),
                ('contact_click', models.IntegerField(default=0)),
                ('contact_start_date', models.CharField(default='', max_length=500)),
                ('contact_end_date', models.CharField(default='', max_length=500)),
                ('success_sign_count', models.IntegerField(default=0)),
                ('success_start_date', models.CharField(default='', max_length=500)),
                ('success_end_date', models.CharField(default='', max_length=500)),
                ('faq_quest_count', models.IntegerField(default=0)),
                ('faq_quest_start_date', models.CharField(default='', max_length=500)),
                ('faq_quest_end_date', models.CharField(default='', max_length=500)),
                ('logout_count', models.IntegerField(default=0)),
                ('logout_start_date', models.CharField(default='', max_length=500)),
                ('logout_end_date', models.CharField(default='', max_length=500)),
                ('charged_count', models.IntegerField(default=0)),
                ('charged_start_date', models.CharField(default='', max_length=500)),
                ('charged_end_date', models.CharField(default='', max_length=500)),
                ('term_click_count', models.IntegerField(default=0)),
                ('term_click_start_date', models.CharField(default='', max_length=500)),
                ('term_click_end_date', models.CharField(default='', max_length=500)),
                ('version_changed_count', models.IntegerField(default=0)),
                ('version_changed_start_date', models.CharField(default='', max_length=500)),
                ('version_changed_end_date', models.CharField(default='', max_length=500)),
                ('pvideo_loaded_count', models.IntegerField(default=0)),
                ('pvideo_loaded_start_date', models.CharField(default='', max_length=500)),
                ('pvideo_loaded_end_date', models.CharField(default='', max_length=500)),
            ],
            options={
                'db_table': 'user_analysis',
            },
        ),
    ]
