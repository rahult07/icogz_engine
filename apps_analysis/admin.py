from django.contrib import admin
from .models import *
# Register your models here.
from import_export.admin import ImportExportModelAdmin

class App_DataAdmin(ImportExportModelAdmin,admin.ModelAdmin):
	list_display =('campaign',)
	ordering =('-campaign',)
	search_fields =('campaign',)
	list_per_page = 100
	list_filter =('campaign',)

class IOS_DataAdmin(ImportExportModelAdmin,admin.ModelAdmin):
	list_display =('campaign',)
	ordering =('-campaign',)
	search_fields =('campaign',)
	list_per_page = 100
	list_filter =('campaign',)

class Adword_DataAdmin(ImportExportModelAdmin,admin.ModelAdmin):
	list_display =('campaign_name',)
	ordering =('-campaign_name',)
	search_fields =('campaign_name',)
	list_per_page = 100
	list_filter =('campaign_name',)

class SubscriptionPlanAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display =('payment_plan',)
    ordering =('-payment_plan',)
    search_fields =('payment_plan',)
    list_per_page = 100
    list_filter =('payment_plan',)

class SubscriptionMethodAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display =('payment_method',)
    ordering =('-payment_method',)
    search_fields =('payment_method',)
    list_per_page = 100
    list_filter =('payment_method',)

admin.site.register(app_data,App_DataAdmin)
admin.site.register(ios_data,IOS_DataAdmin)
admin.site.register(adword_data,Adword_DataAdmin)
admin.site.register(SubscriptionPlan,SubscriptionPlanAdmin)
admin.site.register(SubscriptionMethod,SubscriptionMethodAdmin)