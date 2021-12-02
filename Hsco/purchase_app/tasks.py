from django.contrib import messages
import requests
from .models import *
from django.shortcuts import  redirect
from celery import shared_task

#get customers lat and long stored in database function
@shared_task
def map_all_data():
    geo_api_key = 'AIzaSyAX9a8Sct4E4LN-P0MTJoKzb4iqYodyWdo'

    first_customer_api_count = float(Customer_Details.objects.get(id=8089).api_cal_count)

    customer_list = Customer_Details.objects.filter(
                latitude=None, longitude=None).values_list('address').exclude(address=None).distinct()
    #check if current api count is less than count of customers
    if first_customer_api_count < customer_list.count():
        #iterate through next 1000 customers until last one
        for cust_address in customer_list[first_customer_api_count:first_customer_api_count+1000.0]:
            try:
                response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+str(
                    cust_address) + str(', india')+'&key='+geo_api_key)

                resp_json_payload = response.json()

                latitude = resp_json_payload['results'][0]['geometry']['location']["lat"]
                longitude = resp_json_payload['results'][0]['geometry']['location']["lng"]

                
                Customer_Details.objects.filter(latitude=None,address=cust_address).update(latitude=latitude)
                Customer_Details.objects.filter(longitude=None,address=cust_address).update(longitude=longitude)
            except Exception as e:
                print(resp_json_payload)
                print('exception')
                print(e)
        Customer_Details.objects.filter(id=8089).update(api_cal_count=first_customer_api_count+1000.0)
    return redirect('/modules_map')