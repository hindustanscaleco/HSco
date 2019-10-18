from django.urls import path, include, re_path

from .views import add_ess_details, ess_home, employee_profile, ess_all_user

urlpatterns = [
    path('add_ess_details/',add_ess_details , name ='add_ess_details'),
    path('ess_home/',ess_home , name ='ess_home'),
    path('employee_profile/<int:id>',employee_profile , name ='employee_profile'),
    path('ess_all_user/',ess_all_user , name ='ess_all_user'),
]
