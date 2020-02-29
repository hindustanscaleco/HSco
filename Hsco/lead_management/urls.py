from django.urls import path, include, re_path

from .views import lead_home,view_lead,lead_report,lead_manager_view,lead_follow_up_histroy,lead_delete_product

urlpatterns = [
    path('lead_home/',lead_home , name ='lead_home'),
    path('view_lead/',view_lead , name ='view_lead'),
    path('lead_report/',lead_report , name ='lead_report'),
    path('lead_manager_view/',lead_manager_view , name ='lead_manager_view'),
    path('lead_follow_up_histroy/',lead_follow_up_histroy , name ='lead_follow_up_histroy'),
    path('lead_delete_product/',lead_delete_product , name ='lead_delete_product'),

]
