from django.urls import path, include, re_path

from .views import add_repairing_details, repair_product, repairing_module_home, manager_repairing_module_home

urlpatterns = [
    path('add_repairing_details/',add_repairing_details , name ='add_repairing_details'),
    path('repair_product/',repair_product , name ='repair_product'),
    path('repairing_module_home/',repairing_module_home , name ='repairing_module_home'),
    path('manager_repairing_module_home/',manager_repairing_module_home , name ='manager_repairing_module_home'),
]
