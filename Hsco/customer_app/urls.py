from django.urls import path, include, re_path

from .views import add_customer_details, view_customer_details, update_customer_details, manager_report, report, \
    final_report, add_product_details, employee_sales_graph, feedbacka
from .views import feedback_customer


urlpatterns = [
    path('add_customer_details/',add_customer_details , name ='add_customer_details'),
    path('view_customer_details/',view_customer_details , name ='view_customer_details'),
    path('update_customer_details/<int:id>',update_customer_details, name ='update_customer_details'),
    path('analytics/',manager_report , name ='analytics'),
    path('report/', report, name='report'),
    path('final_report/', final_report, name='final_report'),
    path('manager_report/',manager_report , name ='manager_report'),
    path('employee_sales_graph/',employee_sales_graph , name ='employee_sales_graph'),
    path('feedback_customer/',feedback_customer , name ='feedback_customer'),
    path('add_product_details/<int:id>',add_product_details , name ='add_product_details'),
    path('feedbacka/',feedbacka , name ='feedbacka'),

]
