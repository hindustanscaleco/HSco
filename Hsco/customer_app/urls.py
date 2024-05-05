from django.urls import path, include, re_path

from .views import add_customer_details, update_customer_information, view_customer_information, load_sub_models, load_models, load_sub_sub_models


urlpatterns = [
    path('add_customer_details/', add_customer_details,
         name='add_customer_details'),
    path('view_customer_information/', view_customer_information,
         name='view_customer_information'),
    path('update_customer_information/<int:id>',
         update_customer_information, name='update_customer_information'),

    path('load_models/', load_models, name='load_models'),
    path('load_sub_models/', load_sub_models, name='load_sub_models'),
    path('load_sub_sub_models/', load_sub_sub_models, name='load_sub_sub_models'),


]
