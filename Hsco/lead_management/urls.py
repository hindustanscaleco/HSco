from django.urls import path, include, re_path

from .views import lead_home

urlpatterns = [
    path('lead_home/',lead_home , name ='lead_home'),

]
