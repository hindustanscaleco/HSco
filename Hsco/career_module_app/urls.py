from django.urls import path, include, re_path


from .views import career_module_list,career_module_form,update_career_module_from, career_module_form_hsc


urlpatterns = [
    path('career_module_list/', career_module_list, name ='career_module_list'),
    path('career_module_form/', career_module_form, name ='career_module_form'),
    path('career.hindustanscale.com/', career_module_form_hsc, name ='career_module_form_hsc'),
    path('update_career_module_from/<int:id>', update_career_module_from, name ='update_career_module_from'),
]
