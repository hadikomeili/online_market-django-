from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_list_or_404, reverse, redirect
from django.urls import reverse_lazy
from django.views import View, generic
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .serializers import *

from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from customer.permissions import *


# Create your views here.

# -------------------- FormViews --------------------- #


class OrderItemFormView(generic.FormView):
    template_name = 'order/order_item_form.html'
    form_class = OrderItemForm

    success_url = reverse_lazy('order:add_order_item_form')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# ------------------- Views ----------------------- #


class OrderItemCardView(generic.DetailView):
    """
    View class for card view each order item
    """
    template_name = 'order/order_item_card.html'
    model = OrderItem
    context_object_name = 'order_item_card'


class OrderItemIndexView(generic.TemplateView):
    """
    View class for display all order items
    """
    template_name = 'order/all_order_items.html'
    extra_context = {
        'order_items': OrderItem.objects.all()
    }


class OrderItemDetailView(generic.DetailView):
    """
    View class for display details of an order item
    """
    template_name = 'order/order_item_detail.html'
    model = OrderItem
    context_object_name = 'order_item_detail'


class CartView(LoginRequiredMixin, View):
    """
    View class for Cart
    """

    def get(self, request, *args, **kwargs):
        customer = self.request.user
        customer_order_items = OrderItem.objects.filter(cart__customer=customer)

        return render(request, 'order/cart.html',
                      {'customer': customer, 'customer_order_items': customer_order_items})


# --------------- API Views ------------------ #


class OrderItemListAPIView(generics.ListAPIView):
    """
    API view for superuser to see all order items
    """
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    permission_classes = [
        IsSuperuserPermission
    ]


class CartAPIView(generics.ListAPIView):
    """
    API view for superuser to see all carts
    """
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [
        IsSuperuserPermission
    ]


class CartOrderItemsAPIView(generics.ListCreateAPIView):
    """
    API view for customer to see all order items in his/her cart
    """
    serializer_class = OrderItemForCustomerSerializer
    queryset = OrderItem.objects.all()
    # permission_classes = [
    #     permissions.IsAuthenticated
    # ]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            order_items = OrderItem.objects.filter(cart__customer=self.request.user)
            res = order_items.filter(cart__status='WA')
            return res
        else:
            order_items = OrderItem.objects.filter(cart__customer=None)
            return order_items

    def create(self, request, *args, **kwargs):
        new_order_item = OrderItemForCustomerSerializer(data=request.data)

        if new_order_item.is_valid():
            if Cart.objects.get(customer=request.user):
                new_order_item.validated_data['cart'] = Cart.objects.get(customer=request.user)
                new_order_item.save()
            else:
                Cart.objects.create(customer=request.user)
                new_order_item.validated_data['cart'] = Cart.objects.get(customer=request.user)
                new_order_item.save()

            return Response(new_order_item.data)


class CartOrderItemCreateAPIView(generics.CreateAPIView):
    """
    API view for customer to see all order items in his/her cart
    """
    serializer_class = OrderItemForCustomerSerializer
    queryset = OrderItem.objects.all()
    # permission_classes = [
    #     permissions.IsAuthenticated
    # ]

    # def get_queryset(self):
    #     order_items = OrderItem.objects.filter(cart__customer=self.request.user)
    #     return order_items

    def create(self, request, *args, **kwargs):
        new_order_item = OrderItemForCustomerSerializer(data=request.data)

        if new_order_item.is_valid():
            if request.user.is_authenticated:
                customer = Customer.objects.get(username=request.user.username)
                cart = Cart.objects.filter(customer=customer)

                if not cart or cart[0].status == 'PD':
                    new_cart = Cart.objects.create(customer=customer)
                    new_cart.save()
                    new_order_item.validated_data['cart'] = new_cart
                    new_order_item.save()
                    return Response(new_order_item.data)

                elif cart and cart[0].status == 'WA':
                    new_order_item.validated_data['cart'] = cart[0]
                    new_order_item.save()
                    return Response(new_order_item.data)

            else:
                new_order_item.save()
                return Response(new_order_item.data)


class CartCustomerAPIView(generics.RetrieveUpdateAPIView):
    """
    API view for customer to see his/her cart
    """
    serializer_class = CartForCustomerSerializer
    # queryset = Cart.objects.filter(status='WA', order_address__owner=)

    # def filter_queryset(self, queryset):
    #     x = Cart.objects.filter(order_address__owner=self.request.user)
    #     return x

    def get_object(self):
        queryset = Cart.objects.filter(status='WA')
        queryset2 = Address.objects.all()

        if self.request.user.is_authenticated:
            obj = get_object_or_404(queryset, customer=self.request.user)
            obj.save()
            obj2 = get_list_or_404(queryset2, owner=self.request.user)
            return obj
        else:
            obj = get_object_or_404(queryset, customer=None)
            obj.save()
            return obj


class OrderItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for customer to edit order items in cart
    """
    serializer_class = OrderItemForCustomerSerializer
    queryset = OrderItem.objects.all()
    permission_classes = [
        IsOwnerCartPermission
    ]

    # def get_queryset(self):
    #     order_items = OrderItem.objects.filter(cart__customer=self.request.user)
    #     return order_items


