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

from .views import amc_form, home, login, dashboard
from .views import sidebar, home
from .views import navbar, home
from .views import cust_mod_form, home
from .views import dis_mod_form, home
from .views import ess_form, home
from .views import onsite_rep_form, home
from .views import rep_mod_form, home
from .views import restamping_form, home
from .views import report


urlpatterns = [
path('', dashboard, name='dashboard'),
# path('', home, name='home'),
path('amc_form/', amc_form, name='amc_form'),
path('cust_mod_form/', cust_mod_form, name='cust_mod_form'),
path('dis_mod_form/', dis_mod_form, name='dis_mod_form'),
path('ess_form/', ess_form, name='ess_form'),
path('onsite_rep_form/', onsite_rep_form, name='onsite_rep_form'),
path('rep_mod_form/', rep_mod_form, name='rep_mod_form'),
path('restamping_form/', restamping_form, name='restamping_form'),
path('sidebar/', sidebar, name='sidebar'),
path('navbar/', navbar, name='navbar'),
path('login/', login, name='login'),
path('dashboard/', dashboard, name='dashboard'),
path('report/', report, name='report'),

]
