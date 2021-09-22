import json
from django.utils.translation import to_locale
from rest_framework.views import APIView
from rest_framework import status
from icogz_project.constants import send_response
from rest_framework.decorators import action
import copy
import psycopg2
from .models import *
from django.db.models import Sum, query
from datetime import date, timedelta

def fetch_data_into_pg(postgres_query):
    connection = None
    cursor = None
    records = None
    try:
        connection = psycopg2.connect(user="postgres", password="rahul@123", host="127.0.0.1", port="5432",
                                      database="app_data")
        cursor = connection.cursor()
        cursor.execute(postgres_query)
        row_headers=[x[0] for x in cursor.description]
        records = cursor.fetchall()
        connection.commit()
        print(postgres_query,'\n')
        #print(records)
        return records,row_headers


    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into app table", error)

    
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def remove_end_comma_on_tuple(string_data):
    return str(tuple([string_data])).replace(",","")
    


"""
@descrition: Using drf, Fetch all the contact entries
@return contact log list
"""

class appflyerViewList(APIView):
    """ view all contact data """
    def __init__(self   ):
        self.filter_data = {"all":"('android','ios')",
                       "android":"('android')",
                       "ios":"('ios')"}
        
        self.data = None
        all_data ,paid_data = self.get_medium_data()
        self.medium_source = {
                "organic":"('Organic')",
                "paid":paid_data,
                "all":all_data
        }
    def get(self, request):
        self.from_date = request.POST.get('from_date',None)
        self.to_date = request.POST.get('to_date',None)
        #print(from_date,to_date)
        self.source_type = request.POST.get('source_type',None)
        self.medium_type_data = request.POST.get('medium_type_data',None)
        self.campaign_type = request.POST.get('campaign_type',None)
        self.Media_Source = request.POST.get('Media_Source',None)
        self.b,self.rep_data = self.get_unique_data()
        data = self.fetching_data_quary()
        data_set = self.install_count()
        data_query_set = self.get_date_data()
        query = self.get_ios_data()
        table = self.get_table()
        
        """ response """
        if data:
            return send_response(status.HTTP_200_OK,{"data": data,'data_set':data_set,'data_query_set':data_query_set,'query':query,'table':table}, True, "fetch data successfully")
        else:
            return send_response(status.HTTP_200_OK,{"data": []}, True, "empty_data")


    def fetching_data_quary(self):   
        data,header_names= fetch_data_into_pg(postgres_query="select sum(impressions),sum(clicks),sum(spends) from adword_data")
        for row in data:
            impressions_count = row[0]
            clicks_count = row[1]
            spends_count = row[2]
        data ={'impressions_count':impressions_count,'clicks_count':clicks_count,
                'spends_count':spends_count}
        return data
    
    def install_count(self):
        data_set,header_names = fetch_data_into_pg(postgres_query='select sum(install) from app_data')
        query = ios_data.objects.all().aggregate(install__sum=Sum('install'))['install__sum']
        for row in data_set:
            install_count = row[0]
        
        andriod_ios_count = query + install_count
        #print(install_count,'',query,'','total :-',andriod_ios_count)
        data_set ={'install_count':andriod_ios_count}
        return data_set


    
    def get_medium_data(self):
        query,header_names = fetch_data_into_pg(postgres_query="select distinct(Media_Source) from app_data;")
        all_data = [i for sub in tuple(query) for i in sub]
        paid_data = copy.deepcopy(all_data)
        paid_data.remove('Organic')
        return tuple(all_data),tuple(paid_data)

    def get_unique_data(self):
        query,header_names = fetch_data_into_pg(postgres_query="select distinct(campaign) from app_data;")
        b = [i for sub in tuple(query) for i in sub]
        rep_data = remove_end_comma_on_tuple(self.campaign_type)
        return b,rep_data

    def get_date_data(self):
        if self.from_date and self.to_date:
            data_query_set,header_names= fetch_data_into_pg(postgres_query="select date,sum(impressions),sum(clicks),sum(spends) from adword_data where date between {0} and {1} group by date order by date".format(self.from_date,self.to_date))
        else:
            current_date = date.today()
            dt = date.today() - timedelta(7)
            data_query_set,header_names= fetch_data_into_pg(postgres_query="select date,sum(impressions),sum(clicks),sum(spends) from adword_data where date between '2021-07-25' and '2021-07-31' group by date order by date")
        total_impress =[]
        total_clicks =[]
        total_spends =[]
        data_all =[]
        for data in data_query_set:
            data_all.append(data)
            total_impress.append(data[1])
            total_clicks.append(data[2])
            total_spends.append(data[3])
        impress = sum(total_impress)
        click = sum(total_clicks)
        spends = sum(total_spends)
        data_query_set = {'impress_count':impress,'click_count':click,'spends_count':spends,'data_all':data_all}
        #print(data_all)
        return data_query_set
    
    def get_install_data(self):
        if self.from_date and self.to_date:
            queryset,header_names = fetch_data_into_pg(postgres_query='select date, sum(install) from app_data where date between {0} and {1} group by date order by date'.format(self.from_date,self.to_date))
        else:
            current_date = date.today()
            dt = date.today() - timedelta(7)
            queryset,header_names = fetch_data_into_pg(postgres_query="select date, sum(install) from app_data where date between '2021-07-25' and '2021-07-31' group by date order by date")          
            #queryset ='none'
        total_andriod =[]
        android =[]
        for data in queryset:
            android.append(data[1])
            total_andriod.append(data)

        sum_android = sum(android)
        queryset={"total_android":total_andriod,'sum_android':sum_android}

        return queryset 

    def get_ios_data(self):
        queryset1  = self.get_install_data()
        if self.from_date and self.to_date:
            queryset,header_names = fetch_data_into_pg(postgres_query="select date,sum(install) from public.ios_data where date between {0} and {1} group by date order by date".format(self.from_date,self.to_date))
        else:
            current_date = date.today()
            dt = date.today() - timedelta(7)
            queryset,header_names =fetch_data_into_pg(postgres_query="select date, sum(install) from public.ios_data where date between '2021-07-25' and '2021-07-31' group by date order by date")          
        
        data_install =[]
        data_install_all =[]
        for data in queryset:
            data_install.append(data[1])
            data_install_all.append(data)
        sum_install =sum(data_install)
        total = sum_install + queryset1['sum_android'] 
        #print(sum_install,'',queryset1['sum_android'],'',total)
        queryset ={'total':total}
        return queryset
    
    def get_table(self):
        if self.from_date and self.to_date and self.Media_Source:
            table,header_names =fetch_data_into_pg(postgres_query='''select Campaign_Name,date,sum(impressions) impressions,sum(clicks) click , sum(conversions) install from adword_data 
                                                                    where date between {0} and {1} and source in {2} group by Campaign_Name,date,source order by date '''.format(self.from_date,self.to_date,
                                                                     self.Media_Source['all'] if self.Media_Source is None else remove_end_comma_on_tuple(self.Media_Source)))
            #print('im in table:-',table)
        else:
            table,header_names = fetch_data_into_pg(postgres_query='''select Campaign_Name,date,sum(impressions) impressions,sum(clicks) click , sum(conversions) install 
                                                                        from adword_data where source= 'Google' and date between '2021-07-01' and '2021-07-06'
                                                                        group by Campaign_Name,date,source order by date ''')
        #table={'None'}
        campaign =[]
        date =[]
        impress =[]
        click =[]
        install =[]
        for data in table:
            campaign.append(data[0])
            date.append(data[1])
            impress.append(data[2])
            click.append(data[3])
            install.append(data[4])
        table ={'campaign':campaign,'date':date,'impress':impress,'click':click,'install':install}
        return table

class clevertapViewList(APIView):
    def get(self,request):
        self.from_date = request.POST.get('from_date',None)
        self.to_date = request.POST.get('to_date',None)
        data = self.fetch_Plan()
        dataset =self.fetch_method()
        
        """ response """
        if data:
            return send_response(status.HTTP_200_OK,{"data": data,"dataset":dataset}, True, "fetch data successfully")
        else:
            return send_response(status.HTTP_200_OK,{"data": []}, True, "empty_data")
    
    def fetch_Plan(self):
        if self.from_date and self.to_date:
            query,header_names =fetch_data_into_pg(postgres_query='select date,payment_plan,event_count,people_count,success_count,sale from subscription_plan where date between {0} and {1}'.format(self.from_date,self.to_date))
        else:
            query,header_names =fetch_data_into_pg(postgres_query="select date,payment_plan,event_count,people_count,success_count,sale from subscription_plan where date between '2021-07-01' and '2021-07-06' ")
            print(query)
            #query ={'none'}
        
        date =[]
        payment_plan =[]
        event_count =[]
        people_count =[]
        success_count =[]
        sale =[]
        for data in query:
            date.append(data[0])
            payment_plan.append(data[1])
            event_count.append(data[2])
            people_count.append(data[3])
            success_count.append(data[4])
            sale.append(data[5])

        query ={'date':date,'payment_plan':payment_plan,'event_count':event_count,
                'people_count':people_count,'success_count':success_count,'sale':sale}
        return query

    def fetch_method(self):
        if self.from_date and self.to_date:
            queryset,header_names =fetch_data_into_pg(postgres_query='select date,payment_method,event_count,people_count,success_count from subscription_method where date between {0} and {1}'.format(self.from_date,self.to_date))
        else:
            queryset,header_names =fetch_data_into_pg(postgres_query="select date,payment_method,event_count,people_count,success_count from subscription_method where date between '2021-07-01' and '2021-07-06' ")
            #print(queryset)

        date =[]
        payment_method =[]
        event_count =[]
        people_count =[]
        success_count =[]
        for data in queryset:
            date.append(data[0])
            payment_method.append(data[1])
            event_count.append(data[2])
            people_count.append(data[3])
            success_count.append(data[4])

        queryset ={'date':date,'payment_method':payment_method,'event_count':event_count,
                    'people_count':people_count,'success_count':success_count}
        
        return queryset
    


    