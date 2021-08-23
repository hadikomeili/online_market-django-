from django.urls import path
from .views import *


app_name = 'customer'

urlpatterns = [
    path('api/customer-list/', CustomerListAPIView.as_view(), name='customers_api_for_admin'),
    path('api/customer/details/<int:pk>', CustomerDetailsAdminAPIView.as_view(), name='customer_detail_api_for_admin'),
    path('api/customer-detail/', CustomerDetailAPIView.as_view(), name='customer_detail_api'),
    path('api/addresses/', AddressesIndexAPIView.as_view(), name='addresses_index_api_for_admin'),
    path('api/customer-addresses-list/', AddressListAPIView.as_view(), name='customer_addresses_list_api'),
    path('api/customer-address/<int:pk>', AddressDetailAPIView.as_view(), name='customer_address_detail_api'),
    path('', CustomerIndexView.as_view(), name='all_customers_for_admin'),
    path('addresses/', AddressListView.as_view(), name='all_addresses_for_admin'),
    path('<int:pk>', CustomerDetailView.as_view(), name='customer_details_for_admin'),
    # path('card/<int:pk>', CustomerCardView.as_view(), name='customer_card'),
    path('dashboard/', CustomerDashbordView.as_view(), name='customer_dashboard'),
    # path('detail/<int:pk>', CustomerDetailCardView.as_view(), name='customer_detail'),
    path('dashboard/addresses/<int:pk>', AddressDetailView.as_view(), name='address_detail'),
    path('dashboard/addresses/', AddressListCustomerView.as_view(), name='customer_address_list'),
    path('dashboard/add_address/', AddressCreateFormView.as_view(), name='add_address'),
    path('dashboard/orders/', CustomerCartArchiveIndexView.as_view(), name='customer_cart_archive'),
    path('dashboard/orders/<int:pk>', CustomerCartArchiveDetailsView.as_view(), name='customer_cart_archive_details'),
    path('dashboard/change_password/', change_password, name='change_password'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('signup/', sign_up, name='signup'),


]