from django.urls import path, include, re_path

from .views import add_onsite_aftersales_service, report_onsite, onsite_views, add_onsite_product, \
    update_onsite_details, final_report_onsite, onsite_analytics
from .views import feedback_onrepairing,load_onsite_reparing_stages_list,load_onsite_reparing_manager,onsitevisit_app_graph,update_onsite_product,\
    onsite_repairing_logs


urlpatterns = [
    path('add_onsite_aftersales_service/',add_onsite_aftersales_service , name='add_onsite_aftersales_service'),
    path('report_onsite/',report_onsite, name='report_onsite'),
    path('add_onsite_product/<int:id>',add_onsite_product, name='add_onsite_product'),
    path('update_onsite_product/<int:id>',update_onsite_product, name='update_onsite_product'),
    path('onsite_views/',onsite_views, name='onsite_views'),
    path('report_onsite/',report_onsite, name='report_onsite'),
    path('final_report_onsite/',final_report_onsite, name='final_report_onsite'),
    path('update_onsite_details/<int:id>',update_onsite_details, name='update_onsite_details'),
    path('onsitevisit_app_graph/<str:user_id>',onsitevisit_app_graph, name='onsitevisit_app_graph'),
    path('feedback_onrepairing/<str:user_id>/<str:customer_id>/<str:onsiterepairing_id>',feedback_onrepairing, name='feedback_onrepairing'),
    path('onsitevisit_app_graph/',onsitevisit_app_graph, name='onsitevisit_app_graph'),
    path('load_onsite_reparing_stages_list/', load_onsite_reparing_stages_list, name='load_onsite_reparing_stages_list'),
    path('onsite_analytics/', onsite_analytics, name='onsite_analytics'),
    path('load_onsite_reparing_manager/', load_onsite_reparing_manager, name='load_onsite_reparing_manager'),
    path('onsite_repairing_logs/', onsite_repairing_logs, name='onsite_repairing_logs'),

]
