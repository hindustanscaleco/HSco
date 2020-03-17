from django.urls import path, include, re_path

from .views import Stock_System_View
#add_lead_product

urlpatterns = [
    path('stock_system_view/', Stock_System_View.as_view(), name ='stock_system_view'),
    # path('add_lead_product/<int:id>', add_lead_product, name='add_lead_product'),

]
