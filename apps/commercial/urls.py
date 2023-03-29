from django.urls import path
from apps.commercial.views import *

urlpatterns = [
    path('list_customer_category/', ListCustomerCategory.as_view(), name='list_customer_category'),
    path('create_customer_category/',  CreateCustomerCategory.as_view(), name='create_customer_category'),
    path('edit_customer_category/<pk>/', EditCustomerCategory.as_view(), name='edit_customer_category'),
    path('delete_customer_category/', DeleteCustomerCategory.as_view(), name='delete_customer_category'),

    path('list_customer/', ListCustomer.as_view(), name='list_customer'),
    path('create_customer/',  CreateCustomer.as_view(), name='create_customer'),
    path('edit_customer/<pk>/', EditCustomer.as_view(), name='edit_customer'),
    path('delete_customer/', DeleteCustomer.as_view(), name='delete_customer'),

    path('list_supplier/', ListSupplier.as_view(), name='list_supplier'),
    path('create_supplier/',  CreateSupplier.as_view(), name='create_supplier'),
    path('edit_supplier/<pk>/', EditSupplier.as_view(), name='edit_supplier'),
    path('delete_supplier/', DeleteSupplier.as_view(), name='delete_supplier'),

    path('list_family_group/', ListFamilyGroup.as_view(), name='list_family_group'),
    path('create_family_group/',  CreateFamilyGroup.as_view(), name='create_family_group'),
    path('edit_family_group/<pk>/', EditFamilyGroup.as_view(), name='edit_family_group'),
    path('delete_family_group/', DeleteFamilyGroup.as_view(), name='delete_family_group'),

    path('list_family_activity/', ListFamilyActivity.as_view(), name='list_family_activity'),
    path('create_family_activity/', CreateFamilyActivity.as_view(), name='create_family_activity'),
    path('edit_family_activity/<pk>/', EditFamilyActivity.as_view(), name='edit_family_activity'),
    path('delete_family_activity/', DeleteFamilyActivity.as_view(), name='delete_family_activity'),

    path('list_family/', ListFamily.as_view(), name='list_family'),
    path('create_family/', CreateFamily.as_view(), name='create_family'),
    path('edit_family/<pk>/', EditFamily.as_view(), name='edit_family'),
    path('delete_family/', DeleteFamily.as_view(), name='delete_family'),

    path('list_measurement/', ListMeasurement.as_view(), name='list_measurement'),
    path('create_measurement/', CreateMeasurement.as_view(), name='create_measurement'),
    path('edit_measurement/<pk>/', EditMeasurement.as_view(), name='edit_measurement'),
    path('delete_measurement/', DeleteMeasurement.as_view(), name='delete_measurement'),

    path('list_product/', ListProduct.as_view(), name='list_product'),
    path('create_product/', CreateProduct.as_view(), name='create_product'),
    path('edit_product/<pk>/', EditProduct.as_view(), name='edit_product'),
    path('delete_product/', DeleteProduct.as_view(), name='delete_product'),

    path('list_product_conversion/', ListProductConversion.as_view(), name='list_product_conversion'),
    path('create_product_conversion/', CreateProductConversion.as_view(), name='create_product_conversion'),
    path('edit_product_conversion/<pk>/', EditProductConversion.as_view(), name='edit_product_conversion'),
    path('delete_product_conversion/', DeleteProductConversion.as_view(), name='delete_product_conversion')
]
