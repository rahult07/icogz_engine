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
        connection = psycopg2.connect(user="postgres", password="hitesh@123", host="127.0.0.1", port="5432",
                                      database="app_data")
        cursor = connection.cursor()
        cursor.execute(postgres_query)
        row_headers=[x[0] for x in cursor.description]
        records = cursor.fetchall()
        connection.commit()
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
        self.source_type = request.POST.get('source_type',None)
        self.medium_type_data = request.POST.get('medium_type_data',None)
        self.campaign_type = request.POST.get('campaign_type',None)
        self.Media_Source = request.POST.get('campaign_type',None)
        self.b,self.rep_data = self.get_unique_data()
        data = self.fetching_data_quary()
        """ response """
        if data:
            return send_response(status.HTTP_200_OK,{"data": data}, True, "fetch data successfully")
        else:
            return send_response(status.HTTP_200_OK,{"data": []}, True, "empty_data")


    def fetching_data_quary(self):
        data,header_names = fetch_data_into_pg(postgres_query="SELECT app_data.date,app_data.source_name,app_data.Media_Source,app_data.campaign,app_data.installs,adword_data.Impressions,adword_data.Clicks,adword_data.Conversions FROM app_data JOIN adword_data ON app_data.campaign = adword_data.Campaign_Name where app_data.date between {0} and {1} and app_data.source_name IN {2} and app_data.Media_Source IN {3} and app_data.Media_Source IN {4} and app_data.campaign IN {5};".format(self.from_date,
        self.to_date,
        self.filter_data['all'] if self.source_type is None else self.filter_data[self.source_type],
        self.medium_source['all'] if self.medium_type_data is None else self.medium_source[self.medium_type_data],
        self.medium_source['all'] if self.Media_Source is None else remove_end_comma_on_tuple(self.Media_Source),
        tuple(self.b) if self.campaign_type is None else self.rep_data))
        self.data = data
        print(header_names)

        json_data=[]
        for result in data:
                json_data.append(dict(zip(header_names,result)))
        return json_data

    
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
        

    