from django.urls import path
from .views import *


app_name = 'order'

urlpatterns = [
    path('', OrderItemIndexView.as_view(), name='order_items_index'),
    path('order_item/<int:pk>', OrderItemDetailView.as_view(), name='order_item_detail'),
    path('add_order_item/', OrderItemFormView.as_view(), name='add_order_item_form'),
    path('cart/', CartView.as_view(), name='customer_cart'),
    path('cart/confirmed/', CartConfirmedMessageView.as_view(), name='cart_confirm'),
    path('cart/canceled/', CartCanceledMessageView.as_view(), name='cart_cancel'),
    path('api/orderitems-list/', OrderItemListAPIView.as_view(), name='orderitems_api_for_admin'),
    path('api/cart-list/', CartAPIView.as_view(), name='cart_list_api_for_admin'),
    path('api/cart/', CartCustomerAPIView.as_view(), name='customer_cart_api'),
    path('api/cart/orderitems/', CartOrderItemsAPIView.as_view(), name='customer_cart_orderitems_api'),
    path('api/cart/orderitems/<int:pk>', OrderItemDetailAPIView.as_view(), name='customer_cart_orderitems_details_api'),
    path('api/cart/add_orderitem/', CartOrderItemCreateAPIView.as_view(), name='customer_cart_orderitems_create_api'),
    path('sp_cart/', single_page_cart_view, name='single_page_cart'),

]