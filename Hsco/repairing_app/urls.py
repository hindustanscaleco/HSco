from django.urls import path, include, re_path
from .views import add_repairing_details, repair_product, repairing_module_home, manager_repairing_module_home,load_reparing_stages_list, repairing_analytics
from .views import feedback_repairing,edit_product, repairing_report_module, update_repairing_details, \
    final_repairing_report_module,repairing_employee_graph,load_reparing_manager,load_customer ,load_prev_rep,send_sms

urlpatterns = [
    path('add_repairing_details/',add_repairing_details , name ='add_repairing_details'),
    path('repair_product/<int:id>',repair_product , name ='repair_product'),
    path('repairing_module_home/',repairing_module_home , name ='repairing_module_home'),
    path('manager_repairing_module_home/',manager_repairing_module_home , name ='manager_repairing_module_home'),
    path('repairing_report_module/',repairing_report_module , name ='repairing_report_module'),
    path('final_repairing_report_module/',final_repairing_report_module , name ='final_repairing_report_module'),
    path('update_repairing_details/<int:id>',update_repairing_details , name ='update_repairing_details'),
    path('feedback_repairing/<str:user_id>/<str:customer_id>/<str:repairing_id>',feedback_repairing , name ='feedback_repairing'),
    path('load_reparing_stages_list/',load_reparing_stages_list , name ='load_reparing_stages_list'),
    path('repairing_employee_graph/<str:user_id>',repairing_employee_graph , name ='repairing_employee_graph'),
    path('edit_product/<int:id>',edit_product, name ='edit_product'),
    path('repairing_analytics/',repairing_analytics, name ='repairing_analytics'),
    path('load_reparing_manager/',load_reparing_manager, name ='load_reparing_manager'),
    path('load_customer/',load_customer, name ='load_customer'),
    path('load_prev_rep/',load_prev_rep, name ='load_prev_rep'),
    path('send_sms/',send_sms, name ='send_sms'),
]
