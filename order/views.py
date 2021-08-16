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
        form.cleaned_data['product'] = ...
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
        customer = Customer.objects.get(id=self.request.user.id)
        customer_carts = Cart.objects.filter(customer=customer)
        customer_cart = customer_carts.filter(status='WA')
        if not customer_cart:
            customer_cart = Cart.objects.create(customer=Customer.objects.get(id=customer.id))
            customer_cart.save()

        addresses = Address.objects.filter(owner=customer)

        return render(request, 'order/cart.html',
                      {'customer': customer, 'customer_cart': customer_cart, 'addresses': addresses})

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            address_id = request.POST['address']
            customer = self.request.user
            customer_carts = Cart.objects.filter(customer=customer)
            customer_cart = customer_carts.filter(status='WA')
            for cus in customer_cart:
                cus.order_address = Address.objects.get(id=address_id)
                cus.status = 'PD'
                cus.order_status = 'SN'
                cus.save()

            return redirect('product:product_index')


class CartArchiveView(generic.DetailView):
    template_name = 'order/cart_card.html'
    model = Cart
    context_object_name = 'cart_card'

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
            qs = Cart.objects.filter(status='WA')
            if request.user.is_authenticated:
                customer = Customer.objects.get(username=request.user.username)
                cart = get_object_or_404(qs, customer=customer)

                if not cart or cart.status == 'PD':
                    new_cart = Cart.objects.create(customer=customer)
                    new_cart.save()
                    new_order_item.validated_data['cart'] = new_cart
                    new_order_item.save()
                    return Response(new_order_item.data)

                elif cart and cart.status == 'WA':
                    new_order_item.validated_data['cart'] = cart
                    new_order_item.save()
                    return Response(new_order_item.data)

            else:
                new_order_item.save()
                return Response(new_order_item.data)
    # def create(self, request, *args, **kwargs):
    #     new_order_item = OrderItemForCustomerSerializer(data=request.data)
    #
    #     if new_order_item.is_valid():
    #         customer = Customer.objects.get(id=request.user.id)
    #         cart = Cart.objects.get(customer=customer)
    #         print(cart)
    #
    #         if cart.status == 'WA':
    #
    #             new_order_item.validated_data['cart'] = cart
    #             new_order_item.save()
    #
    #         else:
    #             new_cart = Cart.objects.create(customer=customer)
    #             new_order_item.validated_data['cart'] = new_cart
    #             new_order_item.save()


class CartOrderItemCreateAPIView(generics.CreateAPIView):
    """
    API view for customer to see all order items in his/her cart
    """
    serializer_class = OrderItemForCustomerSerializer
    queryset = OrderItem.objects.filter(cart__status='WA')

    def create(self, request, *args, **kwargs):
        new_order_item = OrderItemForCustomerSerializer(data=request.data)

        if new_order_item.is_valid():
            qs = Cart.objects.filter(status='WA')
            if request.user.is_authenticated:
                customer = Customer.objects.get(username=request.user.username)
                cart = get_object_or_404(qs, customer=customer)

                if not cart or cart.status == 'PD':
                    new_cart = Cart.objects.create(customer=customer)
                    new_cart.save()
                    new_order_item.validated_data['cart'] = new_cart
                    new_order_item.save()
                    return Response(new_order_item.data)

                elif cart and cart.status == 'WA':
                    new_order_item.validated_data['cart'] = cart
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
    queryset = Cart.objects.filter(status='WA')

    def get_object(self):
        queryset = self.queryset

        if self.request.user.is_authenticated:
            customer = Customer.objects.get(id=self.request.user.id)
            print(customer)
            obj = get_object_or_404(queryset, customer=customer)
            obj.save()
            print(obj)
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


# -------------------- Single Page Cart --------------------- #

def single_page_cart_view(request):
    return render(request, 'order/single_page_cart.html')

