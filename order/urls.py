from django.urls import path
from .views import *


app_name = 'order'

urlpatterns = [
    path('', OrderItemIndexView.as_view(), name='order_items_index'),
    path('order_item/<int:pk>', OrderItemDetailView.as_view(), name='order_item_detail'),
    path('add_order_item/', OrderItemFormView.as_view(), name='add_order_item_form'),
    path('cart/', CartView.as_view(), name='customer_cart'),
    path('api/order_items-list/', OrderItemListAPIView.as_view()),
    path('api/cart-list/', CartAPIView.as_view()),

]