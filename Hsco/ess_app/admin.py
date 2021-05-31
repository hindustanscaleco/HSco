from django.contrib import admin

# Register your models here.
from .models import Employee_Leave,Defects_Warning,Employee_Analysis_month,Employee_Analysis_date

class Employee_Analysis_monthAdmin(admin.ModelAdmin):


    list_display = ('id','user_id', 'total_sales_done','total_reparing_done', 'entry_timedate','entry_date',  )
    list_filter = ("user_id","entry_timedate",)

admin.site.register(Employee_Leave)
admin.site.register(Defects_Warning)
admin.site.register(Employee_Analysis_month,Employee_Analysis_monthAdmin)
admin.site.register(Employee_Analysis_date)