from django.contrib import admin
from .models import Career_module, EducationalDetails, WorkExperience, Position
# Register your models here.
class Career_moduleAdmin(admin.ModelAdmin):

    list_display = ('candidate_name','id','phone_no')

    search_fields = ('candidate_name','id','phone_no')

admin.site.register(Career_module, Career_moduleAdmin)
admin.site.register(EducationalDetails)
admin.site.register(WorkExperience)
admin.site.register(Position)
