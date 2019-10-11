from django.urls import path, include, re_path

from .views import add_customer_details, view_customer_details, update_customer_details, manager_report,report, final_report, add_product

urlpatterns = [
    path('add_customer_details/',add_customer_details , name ='add_customer_details'),
    path('view_customer_details/',view_customer_details , name ='view_customer_details'),
    path('update_customer_details/<int:id>',update_customer_details , name ='update_customer_details'),
    path('analytics/',manager_report , name ='analytics'),
    path('report/', report, name='report'),
    path('final_report/', final_report, name='final_report'),
    path('manager_report/',manager_report , name ='manager_report'),
    path('add_product/',add_product , name ='add_product'),
]
