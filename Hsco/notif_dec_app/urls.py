from django.urls import path, include, re_path

from .views import notif_decl_home

urlpatterns = [
    # path('add_dispatch_details/', add_dispatch_details, name ='add_dispatch_details'),
    path('notif_decl_home/', notif_decl_home, name='notif_decl_home'),

]
