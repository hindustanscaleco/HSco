from django.urls import path, include, re_path

from .views import add_customer_details, view_customer_details

urlpatterns = [
    path('add_customer_details/',add_customer_details , name ='add_customer_details'),
    path('view_customer_details/',view_customer_details , name ='view_customer_details'),
]