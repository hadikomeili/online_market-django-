from django.urls import path
from .views import *


app_name = 'customer'

urlpatterns = [
    path('', CustomerListAPIView.as_view(), name='customers_api'),
    path('customer/', CustomerDetailAPIView.as_view(), name='customer_detail_api'),
    path('address/', AddressListAPIView.as_view(), name='address_list_api'),
    path('address/<int:pk>', AddressDetailAPIView.as_view(), name='address_detail_api'),


]