from django.urls import path, include, re_path


from .views import lead_home, add_lead, lead_report, lead_manager_view, lead_follow_up_histroy, lead_delete_product, \
    lead_analytics, \
    lead_employee_graph, update_view_lead, lead_pi_form, select_product

urlpatterns = [
    path('lead_home/',lead_home , name ='lead_home'),
    path('add_lead/',add_lead , name ='add_lead'),
    path('select_product/',select_product , name ='select_product'),
    path('lead_report/',lead_report , name ='lead_report'),
    path('lead_manager_view/',lead_manager_view , name ='lead_manager_view'),
    path('lead_follow_up_histroy/',lead_follow_up_histroy , name ='lead_follow_up_histroy'),
    path('lead_delete_product/<int:id>',lead_delete_product , name ='lead_delete_product'),
    path('lead_analytics/',lead_analytics , name ='lead_analytics'),
    path('lead_employee_graph/',lead_employee_graph , name ='lead_employee_graph'),
    path('update_view_lead/<int:id>',update_view_lead , name ='update_view_lead'),
    path('lead_pi_form/',lead_pi_form , name ='lead_pi_form'),
    path('Pi_section_histroy/',Pi_section_histroy , name ='Pi_section_histroy'),

]
