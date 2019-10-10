from django.urls import path, include, re_path

from .views import add_dispatch_details

urlpatterns = [
    path('add_dispatch_details/',add_dispatch_details , name ='add_dispatch_details'),
]
