from django.urls import path, include, re_path

from .views import add_amc_after_sales,report_amc,amc_views

urlpatterns = [
    path('add_amc_after_sales/',add_amc_after_sales, name ='add_amc_after_sales'),
    path('report_amc/', report_amc, name='report_amc'),
    path('amc_views/', amc_views, name='amc_views'),
]
