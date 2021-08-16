from django.urls import path
from .views import *


app_name = 'product'

urlpatterns = [
    path('', ProductIndexView.as_view(), name='product_index'),
    path('card/<int:pk>', ProductCardView.as_view(), name='product_card'),
    path('<int:pk>', ProductDetailsView.as_view(), name='product_details'),
    path('category/<int:id>', CategoryView.as_view(), name='category_card'),
    # path('products_api/', product_list_view_api, name='products_api'),
    path('api/products/', ProductAPIView.as_view(), name='all_products_api_for_admin'),
    path('api/products/<int:pk>', ProductDetailsAPIView.as_view(), name='product_details_api_for_admin'),
    path('api/products-list/', ProductsIndexAPIView.as_view(), name='products_index_api'),
    path('api/products-list/<int:pk>', ProductDetailsIndexAPIView.as_view(), name='product_details_api'),
    path('api/categories/', CategoryListAPIView.as_view(), name='categories_api_for_admin'),
    path('api/categories/<int:pk>', CategoryDetailAPIView.as_view(), name='categories_details_api_for_admin'),
    path('api/categories-list/', CategoryIndexAPIView.as_view(), name='categories_index_api'),
    path('api/categories-list/<int:pk>', CategoryDetailsIndexAPIView.as_view(), name='category_details_api'),
    path('api/discounts/', DiscountAPIView.as_view(), name='discounts_api_for_admin'),
    path('api/discounts/<int:pk', DiscountDetailAPIView.as_view(), name='discount_detail_api_for_admin'),

]