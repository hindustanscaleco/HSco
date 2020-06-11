from django.urls import path, include, re_path

from .views import stock_godown_list,add_godown,stock_godown,stock_godown_images,stock_good_request,stock_pending_request,stock_transaction_status, \
                    stock_accpet_goods,stock_accpet_goods_list,stock_transaction_history_list,stock_transaction_history, update_godown,\
add_product_godown,request_admin, add_product_master, product_master_list, update_product_master,stock_report

urlpatterns = [
    path('add_product_master/',add_product_master , name ='add_product_master'),
    path('product_master_list/',product_master_list , name ='product_master_list'),
    path('update_product_master/<int:update_id>',update_product_master , name ='update_product_master'),
    path('stock_godown_list/',stock_godown_list , name ='stock_godown_list'),
    path('add_godown/',add_godown, name ='add_godown'),
    path('stock_godown/<str:id>',stock_godown, name ='stock_godown'),
    path('stock_godown_images/',stock_godown_images , name ='stock_godown_images'),
    path('stock_good_request/<int:godown_id>/<int:request_id>',stock_good_request , name ='stock_good_request'),
    path('stock_pending_request/<int:godown_id>',stock_pending_request , name ='stock_pending_request'),
    path('stock_transaction_status/<int:from_godown_id>/<int:trans_id>',stock_transaction_status , name ='stock_transaction_status'),
    path('stock_accpet_goods/<int:godown_id>/<int:accept_id>',stock_accpet_goods , name ='stock_accpet_goods'),
    path('stock_accpet_goods_list/<int:godown_id>',stock_accpet_goods_list , name ='stock_accpet_goods_list'),
    path('stock_transaction_history_list/<int:godown_id>',stock_transaction_history_list , name ='stock_transaction_history_list'),
    path('stock_transaction_history/<int:from_godown_id>/<int:trans_id>',stock_transaction_history , name ='stock_transaction_history'),
    path('update_godown/<int:godown_id>',update_godown , name ='update_godown'),
    path('add_product_godown/<int:godown_id>',add_product_godown , name ='add_product_godown'),
    path('request_admin/',request_admin, name ='request_admin'),
    path('stock_report/',stock_report, name ='stock_report'),

]
