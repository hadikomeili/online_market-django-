from django.shortcuts import render
from django.views import generic, View
from rest_framework import generics
from .serializers import *
from .permissions import *

from .models import *


# Create your views here.

# -------------- Customer -------------- #

class CustomerIndexView(generic.TemplateView):
    """
    View class for display all customers(for superuser use)
    """
    template_name = 'customer/customer_index.html'
    extra_context = {
        'customers': Customer.objects.all(),
    }


class CustomerDetailCardView(generic.DetailView):
    """
    View class for create card view for a customer(for customer use)
    """
    template_name = 'customer/customer_details.html'
    model = Customer
    context_object_name = 'customer_detail'


class CustomerCardView(generic.DetailView):
    """
    View class for create card view for a customer(for superuser use)
    """
    template_name = 'customer/customer_card.html'
    model = Customer
    context_object_name = 'customer_card'


class CustomerDetailView(generic.TemplateView):
    """
    View class for customer dashboard panel
    """
    template_name = 'customer/customer_dashboard.html'
    extra_context = {
        'customers': Customer.objects.all(),
        'category': Category.objects.all().filter(ref_category=None),
    }

# -------------- Address -------------- #


class AddressCardView(generic.DetailView):
    """
    View class for create card view for a address
    """
    template_name = 'customer/address_card.html'
    model = Address
    context_object_name = 'address_card'


class AddressView(generic.TemplateView):
    """
    View class for display all addresses of one customer(based on owner)
    """

    def get(self, request, *args, **kwargs):
        customer = self.request.user
        addresses = Address.objects.filter(owner=customer)

        return render(request, 'customer/address_of_customer.html', {'addresses': addresses})


# ------------------------ API_VIEWS -------------------------- #

class CustomerListAPIView(generics.ListAPIView):
    serializer_class = CustomerBriefListSerializer
    queryset = Customer.objects.all()
    permission_classes = [
        IsSuperuserPermission
    ]


class CustomerDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return self.request.user


class AddressListAPIView(generics.ListAPIView):
    serializer_class = AddressBriefListSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return Address.objects.filter(owner=self.request.user)


class AddressDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    permission_classes = [
        permissions.IsAuthenticated, IsOwnerPermission
    ]
