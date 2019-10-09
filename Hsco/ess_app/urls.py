from django.urls import path, include, re_path

from .views import add_ess_details

urlpatterns = [
    path('add_ess_details/',add_ess_details , name ='add_ess_details'),
]
