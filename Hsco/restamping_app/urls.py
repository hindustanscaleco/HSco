from django.urls import path, include, re_path

from .views import restamping_after_sales_service, report_restamping, restamping_manager, restamping_product,update_restamping_details, final_report_restamping, restamping_employee_graph,load_restamping_manager,update_restamping_product, restamping_analytics

urlpatterns = [
    path('restamping_after_sales_service/', restamping_after_sales_service, name ='restamping_after_sales_service'),
    path('report_restamping/', report_restamping, name='report_restamping'),
    path('final_report_restamping/', final_report_restamping, name='final_report_restamping'),
    path('restamping_manager/', restamping_manager, name='restamping_manager'),
    path('restamping_employee_graph/<str:user_id>', restamping_employee_graph, name='restamping_employee_graph'),
    path('restamping_product/<int:id>', restamping_product, name='restamping_product'),
    path('restamping_analytics/', restamping_analytics, name='restamping_analytics'),
    path('update_restamping_details/<int:id>', update_restamping_details, name='update_restamping_details'),
    path('load_restamping_manager/', load_restamping_manager, name='load_restamping_manager'),
    path('update_restamping_product/<int:id>', update_restamping_product, name='update_restamping_product'),
]
