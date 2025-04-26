from django.contrib import admin
from .models import BMIRecord

@admin.register(BMIRecord)
class BMIRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'bmi_value', 'bmi_category', 'created_at')
    list_filter = ('bmi_category', 'created_at')
    search_fields = ('name', 'email')
    date_hierarchy = 'created_at'