from django.urls import path
from .views import *


app_name = 'product'

urlpatterns = [
    path('', ProductIndexView.as_view(), name='product_index'),
    path('card/<int:pk>', ProductCardView.as_view(), name='product_card'),
    path('<int:pk>', ProductDetailsView.as_view(), name='product_details'),
    path('category/<int:id>', CategoryView.as_view(), name='category_card'),
    path('products_api/', product_list_view_api, name='products_api'),
    path('categories_api/', category_list_view_api, name='categories_api'),
    path('products_api_generic/', ProductAPIView.as_view()),
    path('products_api_generic/<int:pk>', ProductDetailsAPIView.as_view()),

]