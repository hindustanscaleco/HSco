from django.urls import path, include, re_path

from .views import add_onsite_aftersales_service,report_onsite,onsite_views,onsite_reparing_logs

urlpatterns = [
    path('add_onsite_aftersales_service/',add_onsite_aftersales_service , name='add_onsite_aftersales_service'),
    path('report_onsite/',report_onsite, name='report_onsite'),
    path('onsite_views/',onsite_views, name='onsite_views'),
    path('onsite_reparing_logs/',onsite_reparing_logs, name='onsite_reparing_logs'),
]
