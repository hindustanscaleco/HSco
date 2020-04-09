from django.urls import path, include, re_path


from .views import career_module_list,career_module_form,update_career_module_from


urlpatterns = [
    path('career_module_list/', career_module_list, name ='career_module_list'),
    path('career_module_form/', career_module_form, name ='career_module_form'),
    path('update_career_module_from/<int:id>', update_career_module_from, name ='update_career_module_from'),
]
