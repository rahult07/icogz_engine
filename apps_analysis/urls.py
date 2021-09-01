from apps_analysis import views
from django.urls import path

urlpatterns = [
    path('icogz/appflyer', views.appflyerViewList.as_view(), name='appflyer_data'),
]