from django.urls import path, include, re_path

from .views import add_Onsite_aftersales_service

urlpatterns = [
    path('add_onsite_aftersales_service/',add_Onsite_aftersales_service , name='add_onsite_aftersales_service'),
]
