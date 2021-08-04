from django.urls import path
from .views import *


app_name = 'product'

urlpatterns = [
    path('', ProductIndexView.as_view(), name='product_index'),
    path('card/<int:pk>', ProductCardView.as_view(), name='product_card'),
    path('<int:pk>', ProductDetailsView.as_view(), name='product_details'),
    path('category/<int:id>', CategoryView.as_view(), name='category_card'),


]