import json
from rest_framework.views import APIView
from rest_framework import status
from icogz_project.constants import send_response
import copy
import psycopg2


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
    def post(self, request):
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
        """ response """
        if data:
            return send_response(status.HTTP_200_OK,{"data": data,'data_set':data_set}, True, "fetch data successfully")
        else:
            return send_response(status.HTTP_200_OK,{"data": []}, True, "empty_data")


    def fetching_data_quary(self):
        if self.from_date and self.to_date:
            data,header_names= fetch_data_into_pg(postgres_query="select count(impressions),count(clicks),count(conversions),count(spends) from adword_data where date between {0} and {1}".format(self.from_date,self.to_date))
        else: 
            data,header_names= fetch_data_into_pg(postgres_query="select count(impressions),count(clicks),count(conversions),count(spends) from adword_data")
        for row in data:
            impressions_count = row[0]
            clicks_count = row[1]
            conversions_count = row[2]
            spends_count = row[3]
        data ={'impressions_count':impressions_count,'clicks_count':clicks_count,
                'conversions_count':conversions_count,'spends_count':spends_count}
        return data
    
    def install_count(self):
        if self.from_date and self.to_date:
            data_set,header_names = fetch_data_into_pg(postgres_query='select count(installs) from app_data where date between {0} and {1}'.format(self.from_date,self.to_date))
        else:
            data_set,header_names = fetch_data_into_pg(postgres_query='select count(installs) from app_data')
        for row in data_set:
            install_count = row[0]
        data_set ={'install_count':install_count}
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
        

class clevertapViewList(APIView):
    pass
