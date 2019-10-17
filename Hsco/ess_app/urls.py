from django.urls import path, include, re_path

from .views import add_ess_details, ess_home, employee_profile

urlpatterns = [
    path('add_ess_details/',add_ess_details , name ='add_ess_details'),
    path('ess_home/',ess_home , name ='ess_home'),
    path('employee_profile/',employee_profile , name ='employee_profile'),
]
