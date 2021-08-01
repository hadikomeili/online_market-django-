from django.urls import path
from .views import *


app_name = 'product'

urlpatterns = [
    path('/<int:pk>', ProductDetailsView.as_view(), name='product_details'),

]