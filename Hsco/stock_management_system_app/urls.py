from django.urls import path, include, re_path

from .views import stock_godown_list,add_godown,stock_godown,stock_godown_images,stock_good_request,stock_pending_request,stock_transaction_status, \
                    stock_accpet_goods,stock_accpet_goods_list,stock_transaction_history

urlpatterns = [
    path('stock_godown_list/',stock_godown_list , name ='stock_godown_list'),
    path('add_godown/',add_godown, name ='add_godown'),
    path('stock_godown/',stock_godown, name ='stock_godown'),
    path('stock_godown_images/',stock_godown_images , name ='stock_godown_images'),
    path('stock_good_request/',stock_good_request , name ='stock_good_request'),
    path('stock_pending_request/',stock_pending_request , name ='stock_pending_request'),
    path('stock_transaction_status/',stock_transaction_status , name ='stock_transaction_status'),
    path('stock_accpet_goods/',stock_accpet_goods , name ='stock_accpet_goods'),
    path('stock_accpet_goods_list/',stock_accpet_goods_list , name ='stock_accpet_goods_list'),
    path('stock_transaction_history/',stock_transaction_history , name ='stock_transaction_history'),


]
