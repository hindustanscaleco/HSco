from django.urls import path, include, re_path

from .views import add_onsite_aftersales_service,report_onsite,onsite_views,onsite_reparing_logs, add_onsite_product, update_onsite_details, final_report_onsite
from .views import feedback_onrepairing

urlpatterns = [
    path('add_onsite_aftersales_service/',add_onsite_aftersales_service , name='add_onsite_aftersales_service'),
    path('report_onsite/',report_onsite, name='report_onsite'),
    path('add_onsite_product/<int:id>',add_onsite_product, name='add_onsite_product'),
    path('onsite_views/',onsite_views, name='onsite_views'),
    path('onsite_reparing_logs/',onsite_reparing_logs, name='onsite_reparing_logs'),
    path('report_onsite/',report_onsite, name='report_onsite'),
    path('final_report_onsite/',final_report_onsite, name='final_report_onsite'),
    path('update_onsite_details/<int:id>',update_onsite_details, name='update_onsite_details'),
    path('feedback_onrepairing/',feedback_onrepairing, name='feedback_onrepairing'),
]
