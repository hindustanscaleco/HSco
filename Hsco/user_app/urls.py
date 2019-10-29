"""Hsco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from .views import amc_form, home, LoginView,logout_page, dashboard, graph
from .views import sidebar, home
from .views import navbar, home
from .views import user_profile, home
from .views import dis_mod_form, home
from .views import user_logs, home
from .views import onsite_rep_form, home, assign_module_to_emp
from .views import rep_mod_form,  assign_man_to_admin, create_employee, employee_list, assign_emp_to_manager
from .views import restamping_form, home, admin_list, create_admin, create_manager,manager_list,update_admin
from .views import update_manager,update_employee, forgotpassword


urlpatterns = [
# path('', home, name='home'),
path('amc_form/', amc_form, name='amc_form'),
path('user_profile/', user_profile, name='user_profile'),
path('dis_mod_form/', dis_mod_form, name='dis_mod_form'),
path('user_logs/', user_logs, name='user_logs'),
path('onsite_rep_form/', onsite_rep_form, name='onsite_rep_form'),
path('rep_mod_form/', rep_mod_form, name='rep_mod_form'),
path('restamping_form/', restamping_form, name='restamping_form'),
path('sidebar/', sidebar, name='sidebar'),
path('navbar/', navbar, name='navbar'),
path('', LoginView.as_view(), name='login'),
path('logout/', logout_page, name='logout'),
path('dashboard/', dashboard, name='dashboard'),
path('graph/', graph, name='graph'),
path('admin_list/', admin_list, name='admin_list'),
path('create_admin/', create_admin, name='create_admin'),
path('manager_list/', manager_list, name='manager_list'),
path('create_manager/', create_manager, name='create_manager'),
path('assign_man_to_admin/', assign_man_to_admin, name='assign_man_to_admin'),
path('create_employee/', create_employee, name='create_employee'),
path('employee_list/', employee_list, name='employee_list'),
path('assign_emp_to_manager/', assign_emp_to_manager, name='assign_emp_to_manager'),
path('assign_module_to_emp/', assign_module_to_emp, name='assign_module_to_emp'),
path('update_admin/<int:id>',update_admin, name='update_admin'),
path('update_manager/<int:id>',update_manager, name='update_manager'),
path('update_employee/<int:id>',update_employee, name='update_employee'),
path('forgotpassword/', forgotpassword, name='forgotpassword'),

]
