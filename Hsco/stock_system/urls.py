from django.urls import path, include, re_path

from .views import Stock_System_View

urlpatterns = [
    path('stock_system_view/', Stock_System_View.as_view(), name ='stock_system_view'),
]
