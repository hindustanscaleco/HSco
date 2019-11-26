from django.urls import path, include, re_path

from .views import add_dispatch_details, report_dis_mod, dispatch_view, dispatch_logs, final_report_dis_mod, \
    update_dispatch_details, dispatch_employee_graph, load_dispatch_done, load_dispatch_done_manager, \
    dispatch_analytics, load_dispatch_stages_list, edit_dispatch_product

urlpatterns = [
    path('add_dispatch_details/', add_dispatch_details, name ='add_dispatch_details'),
    path('update_dispatch_details/<str:update_id>', update_dispatch_details, name ='update_dispatch_details'),
    path('report_dis_mod/', report_dis_mod, name ='report_dis_mod'),
    path('final_report_dis_mod/', final_report_dis_mod, name ='final_report_dis_mod'),
    path('dispatch_view/', dispatch_view, name ='dispatch_view'),
    path('dispatch_logs/', dispatch_logs, name = 'dispatch_logs'),
    path('dispatch_employee_graph/<str:user_id>', dispatch_employee_graph, name = 'dispatch_employee_graph'),
    path('load_dispatch_done/', load_dispatch_done, name = 'load_dispatch_done'),
    path('load_dispatch_done_manager/', load_dispatch_done_manager, name = 'load_dispatch_done_manager'),
    path('load_dispatch_stages_list/', load_dispatch_stages_list, name = 'load_dispatch_stages_list'),
    path('dispatch_analytics/', dispatch_analytics, name = 'dispatch_analytics'),
    path('edit_dispatch_product/<int:product_id_rec>', edit_dispatch_product, name = 'edit_dispatch_product'),
]
