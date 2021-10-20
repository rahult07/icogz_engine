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
import datetime

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
        self.from_date = request.GET.get('from_date',None)
        self.to_date = request.GET.get('to_date',None)
        #print(from_date,to_date)
        self.source_type = request.POST.get('source_type',None)
        self.medium_type_data = request.POST.get('medium_type_data',None)
        self.campaign_type = request.POST.get('campaign_type',None)
        self.Media_Source = request.GET.get('Media_Source',None)
        self.b,self.rep_data = self.get_unique_data()
        data = self.fetching_data_quary()
        data_set = self.install_count()
        data_query_set = self.get_date_data()
        query = self.get_ios_data()
        table = self.get_table()
        line = self.line_chart()
        
        """ response """
        if data:
            return send_response(status.HTTP_200_OK,{"data": data,'data_set':data_set,'data_query_set':data_query_set,'query':query,'table':table,'line':line}, True, "fetch data successfully")
        else:
            return send_response(status.HTTP_200_OK,{"data": []}, True, "empty_data")


    def fetching_data_quary(self):   
        data,header_names= fetch_data_into_pg(postgres_query='''select sum(impressions),sum(clicks),sum(spends),sum(conversions),extract(year from TO_DATE(date,'YYYY-MM-DD')) date from adword_data group by extract(year from TO_DATE(date,'YYYY-MM-DD')) order by extract(year from TO_DATE(date,'YYYY-MM-DD')) ''')
        datac =[]
        for row in data:
            achived_spends = round((row[2]*1.2)/100,2)
            achived_install = round((row[3]*1.2)/100,2)
            achived_percentage_install = round(row[3]/achived_install,2)
            achived_percentage_spend = round(row[2]/achived_spends,2)
            info ={
                'impressions_count':row[0],
                'clicks_count' :row[1],
                'spends_count' : row[2],
                'install_count' : row[3],
                'year' :int(row[4]),
                'achived_spends':achived_percentage_spend,
                'achived_install':achived_percentage_install

            }
            datac.append(info)
            
        data ={'data_quary':datac}
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
            data_query_set,header_names= fetch_data_into_pg(postgres_query="select date,sum(impressions),sum(clicks),sum(spends),sum(conversions) from adword_data where date between {0} and {1} group by date order by date".format(self.from_date,self.to_date))
        else:
            #current_date = date.today()
            #dt = date.today() - timedelta(7)
            data_query_set,header_names= fetch_data_into_pg(postgres_query="select date,sum(impressions),sum(clicks),sum(spends),sum(conversions) from adword_data where date between '2021-07-01' and '2021-07-06' group by date order by date")
        total_impress =[]
        date_col = []
        total_clicks =[]
        total_spends =[]
        total_install =[]
        data_all =[]
        pervious_date =[]
        for data in data_query_set:
            
            data_all.append(data)
            date_col.append(data[0])
            total_impress.append(data[1])
            total_clicks.append(data[2])
            total_spends.append(data[3])
            total_install.append(data[4])
        
        impress = sum(total_impress)
        click = sum(total_clicks)
        spends = sum(total_spends)
        install = sum(total_install)
        conversion_rate = round((install*100)/click,2)  if install != 0 else 0
        #print('hii percentage :-',conversion_rate)
        
        data_query_set = {'impress_count':impress,'click_count':click,
                          'spends_count':spends,'date':date_col,'all_data':data_all,
                          'impress_data':total_impress,'install_count':install,'conversion_rate':conversion_rate}
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
            table,header_names =fetch_data_into_pg(postgres_query='''select Campaign_Name,date,sum(impressions) impressions,sum(clicks) click , sum(conversions) install,sum(spends) spends from adword_data 
                                                                    where date between {0} and {1} and source in {2} group by Campaign_Name,date,source order by date '''.format(self.from_date,self.to_date,
                                                                     self.Media_Source['all'] if self.Media_Source is None else self.Media_Source))
            #print('im in table:-',self.Media_Source)
        elif self.Media_Source:
            table,header_names = fetch_data_into_pg(postgres_query='''select Campaign_Name,date,sum(impressions) impressions,sum(clicks) click , sum(conversions) install,sum(spends) spends
                                                                        from adword_data where source in {0} and date between '2021-07-01' and '2021-07-06'
                                                                        group by Campaign_Name,date,source order by date '''.format(self.Media_Source['all'] if self.Media_Source is None else self.Media_Source))
        else:
            table,header_names = fetch_data_into_pg(postgres_query='''select Campaign_Name,date,sum(impressions) impressions,sum(clicks) click , sum(conversions) install,sum(spends) spends
                                                                        from adword_data where source ='Google' and date between '2021-07-01' and '2021-07-06'
                                                                        group by Campaign_Name,date,source order by date ''')
            #print(table)
        table_data = []

        for data in table:
            conversion_rate = round((data[4] *100) / data[3],2) if data[4] != 0 else 0
            #print(data[4],'install',data[3],'',conversion_rate)
            #print( data[0],'click here ',round(data[3],2))
            info = {
                'date': data[1],
                'campaign': data[0],
                'impression': data[2],
                'click': data[3],
                'install': data[4],
                'spends':round(data[5],2),
                'conversion_rate': conversion_rate
            }

            table_data.append(info)

        #print(table_data)
        table ={'table_data': table_data}
        #print('table :==============>>',table)
        return table

    def campagin_chart(self):
        campagin ={}
        return campagin
    
    def line_chart(self):
        if self.from_date and self.to_date:
            date = self.from_date.replace('" ',"")
            date_to = self.to_date.replace('" ',"")
            new_to_date = date_to.replace("'","")
            new_date = date.replace("'","")
            date_time_obj = datetime.datetime.strptime(new_date, "%Y-%m-%d") - timedelta(30)
            date_time_obj1 = datetime.datetime.strptime(new_to_date, "%Y-%m-%d") - timedelta(30)
            date_from = date_time_obj.date()
            date_to = date_time_obj1.date()
            #print(new_date,'=====================>',date_from)

            line_data,header_names =fetch_data_into_pg(postgres_query='''select Campaign_Name,date,sum(impressions) impressions,sum(clicks) click , sum(conversions) install,sum(spends) spends from adword_data 
                                                                    where date between {0} and {1}  group by Campaign_Name,date,source order by date '''.format(self.from_date,self.to_date))
                        
            line_data1,header_names =fetch_data_into_pg(postgres_query='''select Campaign_Name,date,sum(impressions) impressions,sum(clicks) click , sum(conversions) install,sum(spends) spends from adword_data 
                                                                    where date between '{0}' and '{1}'  group by Campaign_Name,date,source order by date '''.format(date_from,date_to))
            
        else:
            line_data,header_names =fetch_data_into_pg(postgres_query='''select Campaign_Name,date,sum(impressions) impressions,sum(clicks) click , sum(conversions) install,sum(spends) spends from adword_data 
                                                                    where date between '2021-08-01' and '2021-08-06'  group by Campaign_Name,date,source order by date '''.format(self.from_date,self.to_date))

            line_data1,header_names =fetch_data_into_pg(postgres_query='''select Campaign_Name,date,sum(impressions) impressions,sum(clicks) click , sum(conversions) install,sum(spends) spends from adword_data 
                                                                    where date between '2021-07-01' and '2021-07-06'  group by Campaign_Name,date,source order by date ''')
        data_line =[]
        data_line1=[]
        for line in line_data:
            conversion_rate = round((line[4] *100) / line[3],2) if line[4] != 0 else 0
            line_info ={
                'date':line[1],
                'impressions':line[2],
                'clicks':line[3],
                'install':line[4],
                'conversion_rate':conversion_rate


            }
            data_line.append(line_info)
        for line1 in line_data1:
            conversion_rate = round((line1[4] *100) / line1[3],2) if line1[4] != 0 else 0
            line_info1 ={
                'pervious':line1[1],
                'impressions':line1[2],
                'clicks':line1[3],
                'install':line1[4],
                'conversion_rate':conversion_rate
            }
            data_line1.append(line_info1)
        line_graph ={'data_line':data_line,'data_line1':data_line1}
        return line_graph

class clevertapViewList(APIView):
    def get(self,request):
        self.from_date = request.GET.get('from_date',None)
        self.to_date = request.GET.get('to_date',None)
        self.platform = request.GET.get('platform',None)
        data = self.fetch_Plan()
        dataset =self.fetch_method()
        queryset = self.data_uninstall()
        set_query = self.data_install()
        setquery = self.os_version_fetch()
        app_version = self.app_version_fetch()
        model_name = self.model_fetch()
        device = self.ct_source_fetch()
        
        """ response """
        if data:
            return send_response(status.HTTP_200_OK,{"data": data,"dataset":dataset,
                                                        'queryset':queryset,'set_query':set_query,
                                                        'setquery':setquery,'app_version':app_version,
                                                        'model_name':model_name,'device':device}, True, "fetch data successfully")
        else:
            return send_response(status.HTTP_200_OK,{"data": []}, True, "empty_data")
    
    def fetch_Plan(self):
        if self.from_date and self.to_date:
            query,header_names =fetch_data_into_pg(postgres_query='select date,payment_plan,event_count,people_count,success_count,sale from subscription_plan where date between {0} and {1}'.format(self.from_date,self.to_date))
        else:
            query,header_names =fetch_data_into_pg(postgres_query="select date,payment_plan,event_count,people_count,success_count,sale from subscription_plan where date between '2021-07-01' and '2021-07-06' ")
            #print(query)
            #query ={'none'}
        
        table_data =[]
        
        for data in query:
            success = (data[4] *100) / data[2]  if data[2] != 0 else 0
            info_table ={
                'date':data[0],
                'payment_plan':data[1],
                'event_count':data[2],
                'people_count':data[3],
                'success_count':data[4],
                'sale':data[5],
                'success %':success
            }
            table_data.append(info_table)
        query ={'table_data':table_data}
        return query

    def fetch_method(self):
        if self.from_date and self.to_date:
            queryset,header_names =fetch_data_into_pg(postgres_query='select date,payment_method,event_count,people_count,success_count from subscription_method where date between {0} and {1}'.format(self.from_date,self.to_date))
        else:
            queryset,header_names =fetch_data_into_pg(postgres_query="select date,payment_method,event_count,people_count,success_count from subscription_method where date between '2021-07-01' and '2021-07-06' ")
        
        data_table =[]

        for data in queryset:
            success  = (data[4] *100) / data[2]  if data[2] != 0 else 0
            data_info ={
                'date':data[0],
                'payment_method':data[1],
                'event_count':data[2],
                'people_count':data[3],
                'success_count':data[4],
                'success %':success
            }
            data_table.append(data_info)
        queryset ={'data_table':data_table}
        return queryset

    def data_uninstall(self):
        if self.from_date and self.to_date and self.platform:
            dataset_qu,header =fetch_data_into_pg(postgres_query='''select CAST(timezone('Asia/Kolkata', to_timestamp(uninstall_start_date))AS DATE)  AS Date,
                                                                    count(uninstall_count) from user_analysis 
                                                                        where timezone('Asia/Kolkata', CAST(to_timestamp(uninstall_start_date) AS date)) between {0} and {1} and platform in {2}
                                                                            group by Date order by Date'''.format(self.from_date,self.to_date,
                                                                            self.platform['all'] if self.platform is None else self.platform))
            
            #print(dataset_qu)
        else:
            dataset_qu,header =fetch_data_into_pg(postgres_query='''select CAST(timezone('Asia/Kolkata', to_timestamp(uninstall_start_date))AS DATE)  AS Date, count(uninstall_count) 
                                                                    from user_analysis 
                                                                        where timezone('Asia/Kolkata', CAST(to_timestamp(uninstall_start_date)AS date)) between '2021-09-01' and '2021-09-03' and platform ='Android'
                                                                            group by Date order by Date''')
        data,total_uninstall=[],[]                                                                  
        for rows in dataset_qu:
            total_uninstall.append(rows[1])
            data_col ={
                'date':rows[0],
                'uninstall_count':rows[1]
            }
            data.append(data_col)

        dataset_query = {'data':data,'total_uninstall':sum(total_uninstall)}
        #print('##############',dataset_query)
        return dataset_query
    
    def data_install(self):
        if self.from_date and self.to_date and self.platform:
            data_set,header =fetch_data_into_pg(postgres_query='''select CAST(timezone('Asia/Kolkata', to_timestamp(install_start_date))AS DATE)  AS Date,
                                                                    count(install_count) from user_analysis 
                                                                        where CAST(timezone('Asia/Kolkata', to_timestamp(install_start_date))AS DATE) between {0} and {1} and platform in {2}
                                                                            group by Date order by Date'''.format(self.from_date,self.to_date,
                                                                            self.platform['all'] if self.platform is None else self.platform))
            
            #print(dataset_qu)
        else:
            data_set,header =fetch_data_into_pg(postgres_query='''select CAST(timezone('Asia/Kolkata', to_timestamp(install_start_date))AS DATE)  AS Date, count(install_count) 
                                                                    from user_analysis 
                                                                        where CAST(timezone('Asia/Kolkata', to_timestamp(install_start_date))AS DATE) between '2021-08-31' and '2021-09-03' and platform ='Android'
                                                                            group by Date order by Date''')
        data_seter,total_install =[],[]                                                                   
        for rows in data_set:
            total_install.append(rows[1])
            #print('><<<<>><<<><><><<><><><>',rows[0])
            data_col ={
                'date':rows[0],
                'install_count':rows[1]
            }
            data_seter.append(data_col)

        data_set_query = {'data_set':data_seter,'total_install':total_install}
        #print('##############',data_set_query)
        return data_set_query
    
    def os_version_fetch(self):
        if self.from_date and self.to_date:
            set_query,header = fetch_data_into_pg(postgres_query='''select CAST(timezone('Asia/Kolkata', to_timestamp(app_launched_start_date)) AS DATE)  AS Date,
                                                                os_version,count(os_version) from user_analysis 
                                                                where timezone('Asia/Kolkata', CAST(to_timestamp(app_launched_start_date) AS date))  between {0} and {1} 
                                                                group by os_version,Date order by os_version,Date'''.format(self.from_date,self.to_date))
        else:
            set_query,header = fetch_data_into_pg(postgres_query='''select CAST(timezone('Asia/Kolkata', to_timestamp(app_launched_start_date)) AS DATE)  AS Date,
                                                                os_version,count(os_version) from user_analysis 
                                                                where timezone('Asia/Kolkata', CAST(to_timestamp(app_launched_start_date) AS date))  between '2021-08-31' and '2021-09-07' 
                                                                group by os_version,Date order by os_version,Date''')

        total_os,all_data =[],[] 

        for det in set_query:
            total_os.append(det[2])
            cont ={
                'date':det[0],
                'os_version':det[1],
                'count_os_version':det[2]
            }
            all_data.append(cont)
        setquery ={'all_data':all_data,'total_os':sum(total_os)}
        return setquery
    
    def app_version_fetch(self):
        if self.from_date and self.to_date:
            app_version_data = fetch_data_into_pg(postgres_query='''select CAST(timezone('Asia/Kolkata', to_timestamp(app_launched_start_date)) AS DATE)  AS Date,
                                                                app_version,count(app_version) from user_analysis 
                                                                where timezone('Asia/Kolkata', CAST(to_timestamp(app_launched_start_date) AS date))  between {0} and {1} 
                                                                group by app_version,Date order by app_version,Date'''.format(self.from_date,self.to_date))
        else:
            app_version_data = fetch_data_into_pg(postgres_query='''select CAST(CAST(timezone('Asia/Kolkata', to_timestamp(app_launched_start_date))AS DATE) as character(10)) AS Date, app_version,count(app_version)
                                                                    from user_analysis where CAST(timezone('Asia/Kolkata', to_timestamp(app_launched_start_date))AS DATE) between '2021-08-31' and '2021-09-07' 
                                                                    group by app_version,Date order by app_version,Date''')
        datas = app_version_data[0]
        dat_col,total =[],[]
        for dat in range(len(datas)):
            total.append(datas[dat][2])
            data ={
                'date':datas[dat][0],
                'app_version': datas[dat][1],
                'count_app_version':datas[dat][2],
            }
            dat_col.append(data)
        col_data ={'data':dat_col,'total':sum(total)}
        #print(col_data)
        return col_data

    def model_fetch(self):
        if self.from_date and self.to_date:
            data_model,header = fetch_data_into_pg(postgres_query='''select CAST(timezone('Asia/Kolkata', to_timestamp(app_launched_start_date)) AS DATE)  AS Date,
                                                                model_name,count(model_name) from user_analysis 
                                                                where timezone('Asia/Kolkata', CAST(to_timestamp(app_launched_start_date) AS date))  between {0} and {1} 
                                                                group by model_name,Date order by model_name,Date'''.format(self.from_date,self.to_date))

        else:
            data_model,header = fetch_data_into_pg(postgres_query='''select CAST(timezone('Asia/Kolkata', to_timestamp(app_launched_start_date)) AS DATE)  AS Date,
                                                                model_name,count(model_name) from user_analysis 
                                                                where timezone('Asia/Kolkata', CAST(to_timestamp(app_launched_start_date) AS date))  between '2021-08-31' and '2021-09-07' 
                                                                group by model_name,Date order by model_name,Date''')

        all_model,total_model =[],[]
        for det in data_model:
            column ={
                'date':det[0],
                'models':det[1],
                'count_model':det[2]
            }
            all_model.append(column)
            total_model.append(det[2])
        model_data ={'all_model':all_model,'total_model':sum(total_model)}
        return model_data

    def ct_source_fetch(self):
        if self.from_date and self.to_date:
            ct_data,header = fetch_data_into_pg(postgres_query='''select CAST(timezone('Asia/Kolkata', to_timestamp(app_launched_start_date)) AS DATE)  AS Date,
                                                                ct_source,count(ct_source) from user_analysis 
                                                                where timezone('Asia/Kolkata', CAST(to_timestamp(app_launched_start_date) AS date))  between {0} and {1} 
                                                                group by ct_source,Date order by ct_source,Date'''.format(self.from_date,self.to_date))

        else:
            ct_data,header = fetch_data_into_pg(postgres_query='''select CAST(timezone('Asia/Kolkata', to_timestamp(app_launched_start_date)) AS DATE)  AS Date,
                                                                ct_source,count(ct_source) from user_analysis 
                                                                where timezone('Asia/Kolkata', CAST(to_timestamp(app_launched_start_date) AS date))  between '2021-08-31' and '2021-09-07' 
                                                                group by ct_source,Date order by ct_source,Date''')

        ct_all,total_device =[],[]
        for det in ct_data:
            column={
                'date':det[0],
                'device':det[1],
                'count_device':det[2]
            }
            ct_all.append(column)
            total_device.append(det[2])

        col_device ={'device_data':ct_all,'total_device':sum(total_device)}
        return col_device


#COPY user_analysis FROM '/home/rahul/Music/rahul.csv' DELIMITER ',' CSV HEADER;  