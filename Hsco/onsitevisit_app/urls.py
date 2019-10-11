from django.urls import path, include, re_path

from .views import add_Onsite_visit,add_Onsite_aftersales_service

urlpatterns = [
    path('add_Onsite_visit/',add_Onsite_visit , name='add_Onsite_visit'),
    path('add_Onsite_aftersales_service/',add_Onsite_aftersales_service , name='add_Onsite_aftersales_service'),
]
