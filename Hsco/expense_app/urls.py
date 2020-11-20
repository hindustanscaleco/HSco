from django.urls import path, include
from .views import expense_dashboard,add_expense,expense_product,vendor_master,expense_details,expense_report,expense_report_dashboard,expense_master,expense_type_sub_master,expense_type_sub_sub_master

urlpatterns = [
    path('expense_dashboard/', expense_dashboard, name='expense_dashboard'),
    path('add_expense/', add_expense,name='add_expense'),
    path('expense_product/', expense_product,name='expense_product'),
    path('vendor_master/',vendor_master,name='vendor_master'),
    path('expense_details/',expense_details, name='expense_details'),
    path('expense_report/',expense_report,name='expense_report'),
    path('expense_report_dashboard/',expense_report_dashboard, name='expense_report_dashboard'),
    path('expense_master/',expense_master,name='expense_master'),
    path('expense_type_sub_master/',expense_type_sub_master,name='expense_type_sub_master'),
    path('expense_type_sub_sub_master/',expense_type_sub_sub_master,name='expense_type_sub_sub_master'),
    ]
