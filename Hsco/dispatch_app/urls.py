from django.urls import path, include, re_path

from .views import add_dispatch_details,report_dis_mod, manager_view

urlpatterns = [
    path('add_dispatch_details/',add_dispatch_details, name ='add_dispatch_details'),
    path('report_dis_mod/',report_dis_mod, name ='report_dis_mod'),
    path('manager_view/',manager_view, name ='manager_view'),
]
