from django.urls import path
from apps.accounting.views import *

urlpatterns = [
    path('list_store/', ListStore.as_view(), name='list_store'),
    path('create_store/', CreateStore.as_view(), name='create_store'),
    path('edit_store/<pk>/', EditStore.as_view(), name='edit_store'),
    path('delete_store/', DeleteStore.as_view(), name='delete_store'),

    path('list_area/', ListArea.as_view(), name='list_area'),
    path('create_area/', CreateArea.as_view(), name='create_area'),
    path('edit_area/<pk>/', EditArea.as_view(), name='edit_area'),
    path('delete_area/', DeleteArea.as_view(), name='delete_area'),

    path('list_location/', ListLocation.as_view(), name='list_location'),
    path('create_location/', CreateLocation.as_view(), name='create_location'),
    path('edit_location/<pk>/', EditLocation.as_view(), name='edit_location'),
    path('delete_location/', DeleteLocation.as_view(), name='delete_location'),

    path('list_purchase/', ListPurchase.as_view(), name='list_purchase'),
    path('create_purchase/', CreatePurchase.as_view(), name='create_purchase'),
    path('print_purchase/<pk>/', PrintPurchase.as_view(), name='print_purchase'),

    path('list_sale/', ListSale.as_view(), name='list_sale'),
    path('create_sale/', CreateSale.as_view(), name='create_sale'),
    path('print_sale/<pk>/', PrintSale.as_view(), name='print_sale'),

    path('list_sale_return/', ListSaleReturn.as_view(), name='list_sale_return'),
    path('create_sale_return/', CreateSaleReturn.as_view(), name='create_sale_return'),
    path('print_sale_return/<pk>/', PrintSaleReturn.as_view(), name='print_sale_return'),

    path('list_purchase_return/', ListPurchaseReturn.as_view(), name='list_purchase_return'),
    path('create_purchase_return/', CreatePurchaseReturn.as_view(), name='create_purchase_return'),
    path('print_purchase_return/<pk>/', PrintPurchaseReturn.as_view(), name='print_purchase_return'),

    path('list_positive_adjustment/', ListPositiveAdjustment.as_view(), name='list_positive_adjustment'),
    path('create_positive_adjustment/', CreatePositiveAdjustment.as_view(), name='create_positive_adjustment'),
    path('print_positive_adjustment/<pk>/', PrintPositiveAdjustment.as_view(), name='print_positive_adjustment'),

    path('list_negative_adjustment/', ListNegativeAdjustment.as_view(), name='list_negative_adjustment'),
    path('create_negative_adjustment/', CreateNegativeAdjustment.as_view(), name='create_negative_adjustment'),
    path('print_negative_adjustment/<pk>/', PrintNegativeAdjustment.as_view(), name='print_negative_adjustment'),

    path('list_positive_value_adjustment/', ListPositiveValueAdjustment.as_view(),
         name='list_positive_value_adjustment'),
    path('print_positive_value_adjustment/<pk>/', PrintPositiveValueAdjustment.as_view(),
         name='print_positive_value_adjustment'),

    path('list_negative_value_adjustment/', ListNegativeValueAdjustment.as_view(),
         name='list_negative_value_adjustment'),
    path('print_negative_value_adjustment/<pk>/', PrintNegativeValueAdjustment.as_view(),
         name='print_negative_value_adjustment')
]
