from django.urls import path
from .views import *


app_name = 'customer'

urlpatterns = [
    # path('', CustomerListAPIView.as_view(), name='customers_api'),
    # path('customer/', CustomerDetailAPIView.as_view(), name='customer_detail_api'),
    # path('address/', AddressListAPIView.as_view(), name='address_list_api'),
    # path('address/<int:pk>', AddressDetailAPIView.as_view(), name='address_detail_api'),
    path('', CustomerIndexView.as_view(), name='all_customers'),
    path('card/<int:pk>', CustomerCardView.as_view(), name='customer_card'),
    path('dashboard/', CustomerDetailView.as_view(), name='customer_dashboard'),
    # path('detail/<int:pk>', CustomerDetailCardView.as_view(), name='customer_detail'),
    path('address_detail/<int:pk>', AddressDetailView.as_view(), name='address_detail'),
    path('addresses/', AddressListCustomerView.as_view(), name='address_list'),
    path('add_address/', AddressCreateFormView.as_view(), name='add_address'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('signup/', sign_up, name='signup'),


]