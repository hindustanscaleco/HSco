from django.urls import path, include, re_path

from .views import notif_decl_home, chat_details, chat_with_user,change_replying_status_ajax

urlpatterns = [
    # path('add_dispatch_details/', add_dispatch_details, name ='add_dispatch_details'),
    path('notif_decl_home/', notif_decl_home, name='notif_decl_home'),
    path('chat_details/<str:from_id>/<str:to_id>',chat_details,name='chat_details'),
    path('chat_with_user/',chat_with_user,name='chat_with_user'),
    path('change_replying_status_ajax/<str:user_id>',change_replying_status_ajax,name='change_replying_status_ajax'),
]
