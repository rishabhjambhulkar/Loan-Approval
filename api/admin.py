from django.contrib import admin
from .models import Customer , Loan, Eligibility
# Register your models here.
from import_export.admin import  ImportExportModelAdmin
# admin.py



admin.site.register(Customer, ImportExportModelAdmin)

admin.site.register(Loan, ImportExportModelAdmin)

admin.site.register(Eligibility, ImportExportModelAdmin)