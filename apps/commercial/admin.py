from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import *


class CustomerCategoryResources(resources.ModelResource):
    class Meta:
        model = CustomerCategory


class CustomerCategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'code', 'description', 'discount', 'active')
    search_fields = ['code', 'description']
    resources_class = CustomerCategoryResources


class CustomerResources(resources.ModelResource):
    class Meta:
        model = Customer


class CustomerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'category', 'code', 'description', 'owner', 'address', 'active')
    search_fields = ['category', 'code', 'description', 'owner']
    resources_class = CustomerResources


class SupplierResources(resources.ModelResource):
    class Meta:
        model = Supplier


class SupplierAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'code', 'description', 'owner', 'address', 'active')
    search_fields = ['code', 'description', 'owner']
    resources_class = SupplierResources


class FamilyGroupResources(resources.ModelResource):
    class Meta:
        model = FamilyGroup


class FamilyGroupAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'code', 'description', 'active')
    search_fields = ['code', 'description']
    resources_class = FamilyGroupResources


class FamilyActivityResources(resources.ModelResource):
    class Meta:
        model = FamilyActivity


class FamilyActivityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'code', 'description', 'active')
    search_fields = ['code', 'description']
    resources_class = FamilyActivityResources


class FamilyResources(resources.ModelResource):
    class Meta:
        model = Customer


class FamilyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'group', 'activity', 'code', 'description', 'increment', 'active')
    search_fields = ['group', 'activity', 'code', 'description']
    resources_class = CustomerResources


class MeasurementResources(resources.ModelResource):
    class Meta:
        model = Measurement


class MeasurementAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'code', 'description', 'active')
    search_fields = ['code', 'description']
    resources_class = MeasurementResources


class ProductResources(resources.ModelResource):
    class Meta:
        model = Product


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'family', 'code', 'description', 'measurement', 'sale_price', 'active')
    search_fields = ['family', 'code', 'description']
    resources_class = ProductResources


class ProductConversionResources(resources.ModelResource):
    class Meta:
        model = ProductConversion


class ProductConversionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'product', 'value', 'measurement', 'active')
    search_fields = ['product']
    resources_class = ProductConversionResources


admin.site.register(CustomerCategory, CustomerCategoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(FamilyGroup, FamilyGroupAdmin)
admin.site.register(FamilyActivity, FamilyActivityAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(Measurement, MeasurementAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductConversion, ProductConversionAdmin)
