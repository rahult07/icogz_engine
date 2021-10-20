from django import db
from django.db import models

# Create your models here.

from django.db import models
from django.db.models.base import Model



class app_data(models.Model):
    date = models.TextField(max_length=500)
    country = models.CharField(max_length=500)
    media_source = models.CharField(max_length=200)
    campaign = models.CharField(max_length=200)
    source_name = models.CharField(max_length=200)
    install = models.IntegerField(default=0)

    def __str__(self):
        return self.campaign

    class Meta:
        db_table = 'app_data'


class ios_data(models.Model):
    date = models.TextField(max_length=500)
    country = models.CharField(max_length=500)
    media_source = models.CharField(max_length=200)
    campaign = models.CharField(max_length=200)
    source_name = models.CharField(max_length=200)
    install = models.IntegerField(default=0)

    def __str__(self):
        return self.campaign

    class Meta:
        db_table = 'ios_data'


class adword_data(models.Model):
    date = models.CharField(max_length=255,default='Null')
    product = models.CharField(max_length=255,default='Null')
    campaign_name = models.CharField(max_length=255,default='Null')
    ad_set_name = models.CharField(max_length=255,default='Null')
    ad_name = models.CharField(max_length=255,default='Null')
    impressions = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    spends = models.FloatField(default=0)
    date1 = models.CharField(max_length=255,default='Null')
    srno = models.CharField(max_length=255,default='Null')
    source = models.CharField(max_length=200,default='Null')
    headline1 = models.CharField(max_length=200,default='Null')
    headline2 = models.CharField(max_length=200,default='Null')
    description = models.CharField(max_length=200,default='Null')
    path1 = models.CharField(max_length=200,default='Null')
    path2 = models.CharField(max_length=200,default='Null')
    datetobeconsidered = models.CharField(max_length=200,default='Null')
    icogzclientid = models.CharField(max_length=200,default='Null')
    imageurl = models.CharField(max_length=200,default='Null')
    reach = models.CharField(max_length=200,default='Null')
    modifiedon = models.CharField(max_length=200,default='Null')
    location = models.CharField(max_length=200,default='Null')
    device = models.CharField(max_length=200,default='Null')
    state = models.CharField(max_length=200 ,default='Null')
    views = models.CharField(max_length=200 ,default='Null')
    view_rate = models.CharField(max_length=200 ,default='Null')
    country = models.CharField(max_length=200, default='Null')
    uniqueclicks = models.CharField(max_length=200 ,default='Null')
    video_15_sec_watched = models.CharField(max_length=200 ,default='Null')
    video_30_sec_watched = models.CharField(max_length=200 ,default='Null')
    inline_link_clicks = models.CharField(max_length=200 ,default='Null')
    inline_post_engagement = models.CharField(max_length=200 ,default='Null')
    campaigntype = models.CharField(max_length=200,default='Null')
    mobileappinstall = models.CharField(max_length=200 ,default='Null')

    class Meta:
        db_table ='adword_data'


class SubscriptionPlan(models.Model):
    payment_plan = models.CharField(max_length=255,default='Null')
    date = models.TextField(max_length=500,default='')
    event_count = models.IntegerField(default=0)
    people_count = models.IntegerField(default=0)
    success_count = models.IntegerField(default=0)
    sale = models.IntegerField(default=0)

    class Meta:
        db_table = 'subscription_plan'

class SubscriptionMethod(models.Model):
    payment_method = models.CharField(max_length=255,default='Null')
    date = models.TextField(max_length=500,default='')
    event_count = models.IntegerField(default=0)
    people_count = models.IntegerField(default=0)
    success_count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.payment_method
        
    class Meta:
        db_table = 'subscription_method'



class User_Analysis(models.Model):
    profile_id = models.IntegerField(default=0,null=True,blank=True)
    app_launched_count = models.IntegerField(default=0,null=True,blank=True)
    uninstall_count = models.IntegerField(default=0,null=True,blank=True)
    app_launched_start_date = models.BigIntegerField(default=0,null=True,blank=True)
    app_launched_end_date = models.BigIntegerField(default=0,null=True,blank=True)
    uninstall_start_date = models.BigIntegerField(default=0,null=True,blank=True)
    uninstall_end_date = models.BigIntegerField(default=0,null=True,blank=True)
    install_count = models.IntegerField(default=0,null=True,blank=True)
    install_start_date = models.BigIntegerField(default=0,null=True,blank=True)
    install_end_date = models.BigIntegerField(default=0,null=True,blank=True)
    video_load_count = models.IntegerField(default=0,null=True,blank=True)
    video_load_start_date = models.BigIntegerField(default=0,null=True,blank=True)
    video_load_end_date = models.BigIntegerField(default=0,null=True,blank=True)
    video_progress_count = models.IntegerField(default=0,null=True,blank=True)
    video_progress_start_date = models.BigIntegerField(default=0,null=True,blank=True)
    player_video_progress_end_date = models.BigIntegerField(default=0,null=True,blank=True)
    os_version = models.CharField(max_length=500,default='',null=True,blank=True)
    app_version = models.FloatField(default=0,null=True,blank=True)
    model_name = models.CharField(max_length=500,default='',null=True,blank=True)
    model = models.CharField(max_length=500,default='',null=True,blank=True)
    platform = models.CharField(max_length=500,default='',null=True,blank=True)
    ts = models.CharField(max_length=500,default='',null=True,blank=True)
    ct_app_version = models.FloatField(default=0,null=True,blank=True)
    ct_source = models.CharField(max_length=500,default='',null=True,blank=True)
    menu_click = models.IntegerField(default=0,null=True,blank=True)
    menu_start_date = models.BigIntegerField(default=0,null=True,blank=True)
    menu_end_date = models.BigIntegerField(default=0,null=True,blank=True)
    contact_click = models.IntegerField(default=0,null=True,blank=True)
    contact_start_date =models.BigIntegerField(default=0,null=True,blank=True)
    contact_end_date = models.BigIntegerField(default=0,null=True,blank=True)
    success_sign_count = models.IntegerField(default=0,null=True,blank=True)
    success_start_date =  models.BigIntegerField(default=0,null=True,blank=True)
    success_end_date =  models.BigIntegerField(default=0,null=True,blank=True)
    faq_quest_count = models.IntegerField(default=0,null=True,blank=True)
    faq_quest_start_date =  models.BigIntegerField(default=0,null=True,blank=True)
    faq_quest_end_date =  models.BigIntegerField(default=0,null=True,blank=True)
    logout_count = models.IntegerField(default=0,null=True,blank=True)
    logout_start_date =  models.BigIntegerField(default=0,null=True,blank=True)
    logout_end_date =  models.BigIntegerField(default=0,null=True,blank=True)
    charged_count = models.IntegerField(default=0,null=True,blank=True)
    charged_start_date =  models.BigIntegerField(default=0,null=True,blank=True)
    charged_end_date =  models.BigIntegerField(default=0,null=True,blank=True)
    term_click_count = models.IntegerField(default=0,null=True,blank=True)
    term_click_start_date =  models.BigIntegerField(default=0,null=True,blank=True)
    term_click_end_date =  models.BigIntegerField(default=0,null=True,blank=True)
    version_changed_count = models.IntegerField(default=0,null=True,blank=True)
    version_changed_start_date =  models.BigIntegerField(default=0,null=True,blank=True)
    version_changed_end_date =  models.BigIntegerField(default=0,null=True,blank=True)
    pvideo_loaded_count = models.IntegerField(default=0,null=True,blank=True)
    pvideo_loaded_start_date =  models.BigIntegerField(default=0,null=True,blank=True)
    pvideo_loaded_end_date =  models.BigIntegerField(default=0,null=True,blank=True)

    def __str__(self) -> str:
        return self.profile_id
    class Meta:
        db_table = 'user_analysis'