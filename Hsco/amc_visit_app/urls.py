from django.urls import path, include, re_path

from .views import add_amc_after_sales, add_amcvisit

urlpatterns = [
    path('add_amc_after_sales/',add_amc_after_sales , name ='add_amc_after_sales'),
    path('add_amcvisit/',add_amcvisit , name ='add_amcvisit'),
]
