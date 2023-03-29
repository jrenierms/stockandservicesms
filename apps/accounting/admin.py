from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import *


class StoreResources(resources.ModelResource):
    class Meta:
        model = Store


class StoreAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'code', 'description', 'active')
    search_fields = ['code', 'description']
    resources_class = StoreResources


class AreaResources(resources.ModelResource):
    class Meta:
        model = Area


class AreaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'store', 'code', 'description', 'active')
    search_fields = ['store', 'code', 'description']
    resources_class = AreaResources


class LocationResources(resources.ModelResource):
    class Meta:
        model = Location


class LocationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'area', 'code', 'description', 'active')
    search_fields = ['area', 'code', 'description']
    resources_class = LocationResources


class StockResources(resources.ModelResource):
    class Meta:
        model = Stock


class StockAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'product', 'location', 'cost_price', 'actual_date', 'actual_quantity', 'actual_value')
    search_fields = ['product', 'location', 'cost_price']
    resources_class = StockResources


class TransactionNumberResources(resources.ModelResource):
    class Meta:
        model = TransactionNumber


class TransactionNumberAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'transaction_type', 'number')
    search_fields = ['transaction_type']
    resources_class = TransactionNumberResources


class TransactionSummaryResources(resources.ModelResource):
    class Meta:
        model = TransactionSummary


class TransactionSummaryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'transaction_type', 'supplier', 'customer', 'document', 'source_document', 'date')
    search_fields = ['transaction_type', 'supplier', 'customer', 'document', 'source_document']
    resources_class = TransactionSummaryResources


class TransactionDetailResources(resources.ModelResource):
    class Meta:
        model = TransactionDetail


class TransactionDetailAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'summary', 'product_conversion', 'quantity', 'cost_price', 'sale_price', 'returned_quantity')
    search_fields = ['summary', 'product_conversion', 'cost_price', 'sale_price']
    resources_class = TransactionDetailResources


admin.site.register(Store, StoreAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(TransactionNumber, TransactionNumberAdmin)
admin.site.register(TransactionSummary, TransactionSummaryAdmin)
admin.site.register(TransactionDetail, TransactionDetailAdmin)
