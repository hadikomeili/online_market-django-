from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic, View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response

from order.models import Cart
from .serializers import *
from .permissions import *

from .models import *
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.urls import reverse_lazy


# Create your views here.

# -------------- Customer -------------- #


class CustomerIndexView(LoginRequiredMixin, generic.TemplateView):
    """
    View class for display all customers(for superuser use)
    """
    template_name = 'customer/customer_index.html'
    extra_context = {
        'customers': Customer.objects.all(),
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponse('You have not access to this page!!!')


class CustomerCardView(generic.DetailView):
    """
    View class for create card view for a customer(for superuser use)
    """
    template_name = 'customer/customer_card.html'
    model = Customer
    context_object_name = 'customer_card'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponse('You have not access to this page!!!')


# class CustomerDetailCardView(generic.FormView):
#     """
#     View class for create card view for a customer(for customer use)
#     """
#     template_name = 'customer/customer_details.html'
#     form_class = CustomerForm
#     # context_object_name = 'customer_detail'
#
#     def get(self, request, *args, **kwargs):
#         customer = Customer.objects.get(id=request.user.id)
#         form = CustomerForm(instance=customer)
#         return render(request, 'customer/customer_details.html',
#                       {'form': form})
#
#     def form_valid(self, form):
#         form.save()
#         return super.form_valid(form)


class CustomerTopPanelView(generic.DetailView):
    """
    View class for customer side panel in dashboard
    """
    template_name = 'customer/customer_panel.html'
    model = Customer
    context_object_name = 'customer_panel'


class CustomerDetailView(LoginRequiredMixin, generic.FormView):
    """
    View class for customer dashboard
    """
    template_name = 'customer/customer_details.html'
    form_class = CustomerForm

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(id=request.user.id)
        addresses = Address.objects.filter(owner=customer)
        carts = Cart.objects.filter(customer=customer)
        form = CustomerForm(instance=customer)

        return render(request, 'customer/customer_dashboard.html',
                      {'customer': customer, 'customer_address': addresses, 'carts': carts, 'form': form})

    def form_valid(self, form):
        customer = Customer.objects.get(id=self.request.user.id)
        customer.first_name = form.cleaned_data['first_name']
        customer.last_name = form.cleaned_data['last_name']
        customer.national_code = form.cleaned_data['national_code']
        customer.email = form.cleaned_data['email']
        x = customer.save(update_fields=['first_name', 'last_name', 'national_code', 'email'])
        if x:
            return redirect(reverse_lazy('customer:customer_dashboard'), status=400)
        else:
            return render(self.request, 'customer/customer_dashboard.html',
                          {'customer': customer, 'form': form})


# -------------- Address -------------- #


class AddressCardView(generic.DetailView):
    """
    View class for create card view for a address
    """
    template_name = 'customer/address_card.html'
    model = Address
    context_object_name = 'address_card'


class AddressDetailView(generic.DetailView):
    """
    View class for display address details
    """
    template_name = 'customer/address_detail.html'
    model = Address
    context_object_name = 'address_detail'


class AddressListCustomerView(View):
    """
    View class for display all addresses of one customer(based on owner)
    """

    def get(self, request, *args, **kwargs):
        customer = self.request.user
        addresses = Address.objects.filter(owner=customer)

        return render(request, 'customer/customer_addresses.html', {'customer': customer, 'cus_addresses': addresses})


# ------------------------ Form View --------------------------- #


class AddressCreateFormView(generic.FormView):
    template_name = 'customer/create_address.html'
    form_class = AddressForm

    success_url = reverse_lazy('customer:address_list')

    def form_valid(self, form):

        new_address = form.save()
        new_address.owner = Customer.objects.get(id=self.request.POST['owner'])
        new_address.save()
        return super().form_valid(form)


# ------------------------ API_VIEWS -------------------------- #


class CustomerListAPIView(generics.ListAPIView):
    """
    API view for superuser to see list of customers
    """
    serializer_class = CustomerBriefListSerializer
    queryset = Customer.objects.all()
    permission_classes = [
        IsSuperuserPermission
    ]


class CustomerDetailsAdminAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for superuser to edit and delete customer
    """
    serializer_class = CustomerDetailAdminSerializer
    queryset = Customer.objects.all()
    permission_classes = [
        IsSuperuserPermission
    ]


class CustomerDetailAPIView(generics.RetrieveUpdateAPIView):
    """
    API view for customer to see and update his info
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, username=self.request.user)
        return obj


class AddressListAPIView(generics.ListCreateAPIView):
    """
    for customer use
    """
    serializer_class = AddressDetailSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return Address.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        new_address = AddressDetailSerializer(data=request.data)

        if new_address.is_valid():
            new_address.validated_data['owner'] = Customer.objects.get(phone=request.user.phone)
            # print(type(new_address.validated_data))
            new_address.save()

            return Response(new_address.data)


class AddressDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    for customer use
    """
    serializer_class = AddressDetailSerializer
    queryset = Address.objects.all()
    permission_classes = [
        permissions.IsAuthenticated, IsOwnerAddressPermission
    ]


class AddressesIndexAPIView(generics.ListAPIView):
    """
    for superuser use
    """
    serializer_class = AddressBriefListSerializer
    queryset = Address.objects.all()
    permission_classes = [
        IsSuperuserPermission, permissions.IsAuthenticated
    ]


# -------------------- login/logout/signup ---------------------- #


class MyLoginView(LoginView):
    pass


class MyLogoutView(LogoutView):
    pass


def sign_up(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            phone = form.cleaned_data.get('phone')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, phone=phone, password=password)
            login(request, user)
            return redirect('customer:customer_dashboard')
    else:
        form = MyUserCreationForm()
    return render(request, 'customer/signup.html', {'form': form})

# def home(request):
#     return render(request, 'home.html')
