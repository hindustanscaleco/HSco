from django.urls import path, include, re_path

from .views import add_repairing_details

urlpatterns = [
    path('add_repairing_details/',add_repairing_details , name ='add_repairing_details'),
]
