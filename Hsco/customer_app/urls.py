from django.urls import path, include, re_path

from .views import add_customer_details, view_customer_details, update_customer_details, manager_report

urlpatterns = [
    path('add_customer_details/',add_customer_details , name ='add_customer_details'),
    path('view_customer_details/',view_customer_details , name ='view_customer_details'),
    path('update_customer_details/<int:id>',update_customer_details , name ='update_customer_details'),
    path('manager_report/',manager_report , name ='manager_report'),
]
