from django.urls import path, include, re_path


from .views import lead_home, add_lead, lead_report, lead_manager_view, lead_follow_up_histroy, lead_delete_product, \
    lead_analytics, \
    lead_employee_graph, update_view_lead, lead_pi_form, select_product, pi_section_history, alpha_pi_form, \
    select_product_followup, final_lead_report, download_pi_image, download_pi_pdf, report_2


urlpatterns = [
    path('lead_home/',lead_home , name ='lead_home'),
    path('add_lead/',add_lead , name ='add_lead'),
    path('select_product/<int:id>',select_product , name ='select_product'),
    path('select_product_followup/<int:id>',select_product_followup , name ='select_product_followup'),
    path('lead_report/',lead_report , name ='lead_report'),
    path('lead_manager_view/',lead_manager_view , name ='lead_manager_view'),
    path('lead_follow_up_histroy/<int:follow_up_id>',lead_follow_up_histroy , name ='lead_follow_up_histroy'),
    path('lead_delete_product/<int:id>',lead_delete_product , name ='lead_delete_product'),
    path('lead_analytics/',lead_analytics , name ='lead_analytics'),
    path('lead_employee_graph/<int:id>',lead_employee_graph , name ='lead_employee_graph'),
    path('update_view_lead/<int:id>',update_view_lead , name ='update_view_lead'),
    path('lead_pi_form/',lead_pi_form , name ='lead_pi_form'),
    path('pi_section_history/<int:id>',pi_section_history , name ='pi_section_history'),
    path('alpha_pi_form/',alpha_pi_form , name ='alpha_pi_form'),
    path('report_2/',report_2 , name ='report_2'),
    path('final_lead_report/',final_lead_report , name ='final_lead_report'),
    path('download_pi_image/',download_pi_image , name ='download_pi_image'),
    path('download_pi_pdf/',download_pi_pdf , name ='download_pi_pdf'),

]
