from django.urls import path, include, re_path

from .views import lead_home,view_lead,lead_report

urlpatterns = [
    path('lead_home/',lead_home , name ='lead_home'),
    path('view_lead/',view_lead , name ='view_lead'),
    path('lead_report/',lead_report , name ='lead_report'),

]
