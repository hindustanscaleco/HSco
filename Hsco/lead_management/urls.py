from django.urls import path, include, re_path


from .views import lead_home, add_lead, lead_report, lead_manager_view, lead_follow_up_histroy, lead_delete_product, \
    lead_analytics, \
    lead_employee_graph, update_view_lead, lead_pi_form, select_product, pi_section_history, alpha_pi_form, \
    select_product_followup, final_lead_report, download_pi_image, download_pi_pdf, report_2, lead_logs, \
    download_pi_second_pdf,followup_delete_product,upload_requirement_hsc, final_lead_report_test, get_pi_product_details


urlpatterns = [
    path('lead_home/',lead_home , name ='lead_home'),
    path('add_lead/',add_lead , name ='add_lead'),
    path('select_product/<int:id>',select_product , name ='select_product'),
    path('select_product_followup/<int:id>',select_product_followup , name ='select_product_followup'),
    path('lead_report/',lead_report , name ='lead_report'),
    path('lead_manager_view/',lead_manager_view , name ='lead_manager_view'),
    path('lead_follow_up_histroy/<int:follow_up_id>',lead_follow_up_histroy , name ='lead_follow_up_histroy'),
    path('lead_delete_product/<int:id>',lead_delete_product , name ='lead_delete_product'),
    path('followup_delete_product/<int:id>',followup_delete_product , name ='followup_delete_product'),
    path('lead_analytics/',lead_analytics , name ='lead_analytics'),
    path('lead_employee_graph/<int:id>',lead_employee_graph , name ='lead_employee_graph'),
    path('update_view_lead/<int:id>',update_view_lead , name ='update_view_lead'),
    path('lead_pi_form/',lead_pi_form , name ='lead_pi_form'),
    path('pi_section_history/<int:id>',pi_section_history , name ='pi_section_history'),
    path('alpha_pi_form/',alpha_pi_form , name ='alpha_pi_form'),
    path('report_2/',report_2 , name ='report_2'),
    path('final_lead_report/',final_lead_report , name ='final_lead_report'),
    path('final_lead_report_test/',final_lead_report_test , name ='final_lead_report_test'),
    path('download_pi_image/<int:id>',download_pi_image , name ='download_pi_image'),
    path('download_pi_pdf/<int:id>/<int:download>',download_pi_pdf , name ='download_pi_pdf'), #<int:download> == 1 Download = True else Download = False
    path('download_pi_second_pdf/<int:id>/<int:download>',download_pi_second_pdf , name ='download_pi_second_pdf'), #<int:download> == 1 Download = True else Download = False
    path('lead_logs/',lead_logs , name ='lead_logs'),
    path('get_pi_product_details/',get_pi_product_details , name ='get_pi_product_details'),
    path('requirement.hindustanscale.com/',upload_requirement_hsc , name ='upload_requirement_hsc'),

]
