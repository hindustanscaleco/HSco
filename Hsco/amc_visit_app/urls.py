from django.urls import path, include, re_path


from .views import add_amc_after_sales,report_amc,amc_views,update_amc_form,final_report_amc,amc_logs

urlpatterns = [
    path('add_amc_after_sales/',add_amc_after_sales, name ='add_amc_after_sales'),
    path('report_amc/', report_amc, name='report_amc'),
    path('final_report_amc/', final_report_amc, name='final_report_amc'),
    path('amc_views/', amc_views, name='amc_views'),
    path('amc_logs/', amc_logs, name='amc_logs'),
    path('update_amc_form/<str:update_id>', update_amc_form, name='update_amc_form'),
]
