from django.urls import path, include, re_path

from .views import add_onsite_aftersales_service,report_onsite

urlpatterns = [
    path('add_onsite_aftersales_service/',add_onsite_aftersales_service , name='add_onsite_aftersales_service'),
    path('report_onsite/',report_onsite, name='report_onsite'),
]
