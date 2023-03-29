from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Setting


class SettingResources(resources.ModelResource):
    class Meta:
        model = Setting


class SettingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'company_code', 'company_description', 'company_address', 'company_email', 'logo')
    search_fields = ['company_code', 'company_description']
    resources_class = SettingResources


admin.site.register(Setting, SettingAdmin)
