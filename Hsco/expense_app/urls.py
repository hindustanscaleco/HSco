from django.urls import path, include
from .views import expense_dashboard,add_expense,expense_product,vendor_master,expense_details,expense_report, \
expense_report_dashboard,expense_master,expense_type_sub_master,expense_type_sub_sub_master, load_expense_sub_master, load_expense_sub_sub_master, \
    load_vendor_details,load_expense_by_company, final_expense_report, update_expense_product, update_expense_type_sub_master, \
        update_expense_type_sub_sub_master,showBill

urlpatterns = [
    path('expense_dashboard/', expense_dashboard, name='expense_dashboard'),
    path('add_expense/', add_expense,name='add_expense'),
    path('expense_product/<str:expense_id>', expense_product,name='expense_product'),
    path('vendor_master/',vendor_master,name='vendor_master'),
    path('expense_details/<str:expense_id>',expense_details, name='expense_details'),
    path('expense_report/',expense_report,name='expense_report'),
    path('expense_report_dashboard/',expense_report_dashboard, name='expense_report_dashboard'),
    path('expense_master/',expense_master,name='expense_master'),
    path('expense_type_sub_master/',expense_type_sub_master,name='expense_type_sub_master'),
    path('expense_type_sub_sub_master/',expense_type_sub_sub_master,name='expense_type_sub_sub_master'),
    path('load_expense_sub_master/',load_expense_sub_master,name='load_expense_sub_master'),
    path('load_expense_sub_sub_master/',load_expense_sub_sub_master,name='load_expense_sub_sub_master'),
    path('load_vendor_details/',load_vendor_details,name='load_vendor_details'),
    path('load_expense_by_company/',load_expense_by_company,name='load_expense_by_company'),
    path('final_expense_report/',final_expense_report,name='final_expense_report'),
    path('update_expense_product/<str:expense_id>/<str:product_id>',update_expense_product,name='update_expense_product'),
    path('update_expense_type_sub_master/<str:sub_master_id>/',update_expense_type_sub_master,name='update_expense_type_sub_master'),
    path('update_expense_type_sub_sub_master/<str:sub_master_id>/',update_expense_type_sub_master,name='update_expense_type_sub_master'),
    path('showBill/',showBill,name='showBill'),
    ]
