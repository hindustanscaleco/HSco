from django.urls import path, include, re_path

from .views import add_purchase_details, view_customer_details, update_customer_details, manager_report, report, \
    final_report, add_product_details, customer_employee_sales_graph, feedbacka, purchase_analytics
from .views import feedback_purchase, autocomplete
from .views import edit_product_customer,load_users, purchase_logs, stock_does_not_exist, quick_purchase_entry,get_product_details



urlpatterns = [
    path('add_purchase_details/',add_purchase_details , name ='add_purchase_details'),
    path('view_customer_details/',view_customer_details , name ='view_customer_details'),
    path('update_customer_details/<int:id>',update_customer_details, name ='update_customer_details'),
    path('report/', report, name='report'),
    path('final_report/', final_report, name='final_report'),
    path('manager_report/',manager_report , name ='manager_report'),
    path('customer_employee_sales_graph/<str:user_id>',customer_employee_sales_graph , name ='customer_employee_sales_graph'),
    path('feedback_purchase/<str:user_id>/<str:customer_id>/<str:purchase_id>',feedback_purchase , name ='feedback_purchase'),
    path('add_product_details/<int:id>',add_product_details, name ='add_product_details'),
    path('feedbacka/',feedbacka, name ='feedbacka'),
    path('edit_product_customer/<int:product_id_rec>',edit_product_customer, name = 'edit_product_customer'),
    path('purchase_analytics/',purchase_analytics, name = 'purchase_analytics'),
    path('load_users/',load_users, name = 'load_users'),
    path('purchase_logs/',purchase_logs, name = 'purchase_logs'),
    path('stock_does_not_exist/',stock_does_not_exist, name = 'stock_does_not_exist'),
    path('quick_purchase_entry/',quick_purchase_entry, name = 'quick_purchase_entry'),
    path('get_product_details/',get_product_details, name = 'get_product_details'),
    path('autocomplete/',autocomplete, name = 'ajax_autocomplete'),

]
