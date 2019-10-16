from django.urls import path, include, re_path

from .views import add_ess_details, ess_home, employee_profile, ess_all_user, notif_decl_home

urlpatterns = [
    path('add_ess_details/',add_ess_details , name ='add_ess_details'),
    path('ess_home/',ess_home , name ='ess_home'),
    path('employee_profile/',employee_profile , name ='employee_profile'),
    path('ess_all_user/',ess_all_user , name ='ess_all_user'),
    path('notif_decl_home/',notif_decl_home , name ='notif_decl_home'),
]
