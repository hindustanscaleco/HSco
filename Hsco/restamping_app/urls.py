from django.urls import path, include, re_path

from .views import restamping_after_sales_service

urlpatterns = [
    path('restamping_after_sales_service/',restamping_after_sales_service , name ='restamping_after_sales_service'),
]
