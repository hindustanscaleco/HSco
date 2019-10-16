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

from .views import amc_form, home, login, dashboard, graph
from .views import sidebar, home
from .views import navbar, home
from .views import user_profile, home
from .views import dis_mod_form, home
from .views import user_logs, home
from .views import onsite_rep_form, home
from .views import rep_mod_form,  assign_man_to_admin
from .views import restamping_form, home, admin_list, create_admin, create_manager,manager_list


urlpatterns = [
path('', dashboard, name='dashboard'),
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
path('login/', login, name='login'),
path('dashboard/', dashboard, name='dashboard'),
path('graph/', graph, name='graph'),
path('admin_list/', admin_list, name='admin_list'),
path('create_admin/', create_admin, name='create_admin'),
path('manager_list/', manager_list, name='manager_list'),
path('create_manager/', create_manager, name='create_manager'),
path('assign_man_to_admin/', assign_man_to_admin, name='assign_man_to_admin'),

]
