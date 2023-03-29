from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import *


class UserResources(resources.ModelResource):
    class Meta:
        model = User


class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'id_card', 'username', 'first_name', 'last_name', 'gender', 'image', 'email', 'address',
                    'landline', 'mobile_phone')
    search_fields = ['username']
    resources_class = UserResources


class AuditResources(resources.ModelResource):
    class Meta:
        model = Audit


class AuditAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'access', 'date_time', 'comment',)
    search_fields = ['user']
    resources_class = AuditResources


admin.site.register(User, UserAdmin)
admin.site.register(Audit, AuditAdmin)
