from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_list_or_404, reverse, redirect
from django.urls import reverse_lazy
from django.views import View, generic
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.utils.translation import gettext as _

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

    def post(self, request, *arg, **kwargs):
        resp = JsonResponse({"msg": "product added to your cart!"})
        product = request.POST.get("product")
        product_number = request.POST.get("product_number")
        cart = request.COOKIES.get("cart", "")
        resp.set_cookie("cart", cart + product + ":" + product_number + ",")
        return resp


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
    template_name = 'order/orderitem_card_for_cart.html'
    model = OrderItem
    context_object_name = 'order_item_detail'


class CartView(LoginRequiredMixin, View):
    """
    View class for Cart
    """

    def get(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.get(id=self.request.user.id)
        except Customer.DoesNotExist:
            return redirect(reverse('customer:login'))
        addresses = Address.objects.filter(owner=customer)
        if addresses.count() == 0:
            return redirect(reverse('customer:add_address'),
                            {'msg': _('please add an address for sending your orders!')})
        new_orderitems = set(request.COOKIES.get("cart", "").split(","))

        customer_carts = Cart.objects.filter(customer=customer)
        customer_cart = customer_carts.filter(status='WA')
        if customer_cart.count() == 1:
            cart = customer_cart[0]

        else:
            cart = Cart.objects.create(customer=customer)
            cart.save()

        if not new_orderitems == {''}:
            for orderitem in new_orderitems:

                items_in_cart = OrderItem.objects.filter(cart=cart)
                if items_in_cart:
                    if not orderitem == '':
                        product_id, p_number = orderitem.split(":")

                        for item in items_in_cart:

                            if int(product_id) == item.product.id:
                                num = item.product_number
                                num += int(p_number)
                                item.product_number = num
                                product = item.product
                                product.inventory -= int(p_number)
                                product.save()
                                item.save()
                                cart.save()
                                # msg = _('product updated in ')
                            else:
                                o_item = OrderItem.objects.create(product=Product.objects.get(id=product_id),
                                                                  product_number=int(p_number), cart=cart)
                                o_item.save()
                                product = o_item.product
                                product.inventory -= int(p_number)
                                product.save()
                                cart.save()

                    else:
                        continue
                else:
                    if not orderitem == '':
                        product_id, p_number = orderitem.split(":")
                        o_item = OrderItem.objects.create(product=Product.objects.get(id=product_id),
                                                          product_number=int(p_number), cart=cart)
                        o_item.save()
                        product = o_item.product
                        product.inventory -= int(p_number)
                        product.save()
                        cart.save()

        cart.save()
        cart_orderitems = OrderItem.objects.filter(cart=cart)
        response = render(request, 'order/cart.html',
                          {'customer': customer, 'customer_cart': cart, 'addresses': addresses,
                           'orderitems': cart_orderitems})

        response.set_cookie("cart", '')
        return response

    def post(self, request, *args, **kwargs):
        pprint(request.POST)

        customer = Customer.objects.get(id=self.request.user.id)
        customer_carts = Cart.objects.filter(customer=customer)
        customer_cart = customer_carts.filter(status='WA')
        cart = customer_cart[0]               # it can change and line bala!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
        # orderitems = OrderItem.objects.get(cart=cart)

        # addresses = cart.order_address
        if 'confirm' in request.POST:
            confirm = request.POST['confirm']
            if confirm == 'Confirm and Pay':
                if not cart.final_price == 0:
                    address_id = request.POST['address']
                    cart.order_address = Address.objects.get(id=address_id)
                    cart.save()
                    cart.status = 'PD'
                    cart.order_status = 'SN'
                    cart.save()
                    msg = _('Thanks for your trust. Your order successfully registered.'
                            ' Our staff will call you for sending your order.')
                    return HttpResponse(msg)
                else:
                    msg = _('Your cart is empty!!!')
                    return HttpResponse(msg)

        elif 'cancel' in request.POST:
            cancel = request.POST['cancel']
            if cancel == 'Cancel Order':
                if not cart.final_price == 0:
                    orderitems = OrderItem.objects.filter(cart=cart)
                    # print(orderitems)
                    for orderitem in orderitems:
                        product = orderitem.product
                        product.inventory += orderitem.product_number
                        product.save()
                        orderitem.deleted = True
                        orderitem.save()
                    cart.status = 'CA'
                    cart.order_status = 'CA'
                    cart.deleted = True
                    cart.save()
                    msg = _('This order canceled successfully!')
                    return HttpResponse(msg)
                else:
                    msg = _('Your cart is empty!!!')
                    return HttpResponse(msg)

        elif 'update' in request.POST:
            update = request.POST['update']
            if update == 'update':
                new_number = request.POST['number']
                print(new_number)
                orderitem_id = request.POST['orderitem_id']
                new_orderitem = OrderItem.objects.get(id=orderitem_id)
                product = new_orderitem.product
                product_number = new_orderitem.product_number
                product.inventory -= (int(new_number) - int(product_number))
                product.save()
                new_orderitem.product_number = int(new_number)
                new_orderitem.save()
                print(new_orderitem)
                cart.save()
                cart_orderitems = OrderItem.objects.filter(cart=cart)
                addresses = Address.objects.filter(owner=customer)

                return render(request, 'order/cart.html',
                          {'customer': customer, 'customer_cart': cart, 'addresses': addresses,
                           'orderitems': cart_orderitems})
        elif 'delete' in request.POST:
            delete = request.POST['delete']
            if delete == 'delete':
                number = request.POST['number']
                orderitem_id = request.POST['orderitem_id']
                new_orderitem = OrderItem.objects.get(id=orderitem_id)
                product = new_orderitem.product
                product.inventory += int(number)
                product.save()
                new_orderitem.deleted = True
                new_orderitem.save()
                cart.save()
                cart_orderitems = OrderItem.objects.filter(cart=cart)
                addresses = Address.objects.filter(owner=customer)

                return render(request, 'order/cart.html',
                          {'customer': customer, 'customer_cart': cart, 'addresses': addresses,
                           'orderitems': cart_orderitems})

class CartArchiveCardView(generic.DetailView):
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
    form = OrderItemForm
    customer = Customer.objects.get(id=request.user.id)
    orderitems = OrderItem.objects.filter(cart__status='WA').get(cart=Cart.objects.get(customer=customer))
    # o_items = orderitems.filter(cart__status="WA")

    return render(request, 'order/single_page_cart.html', {'form': form, 'orderitems': orderitems})
