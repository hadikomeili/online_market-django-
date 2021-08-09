from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm
    list_display = ('first_name', 'last_name', 'phone', 'email', 'national_code', 'gender')
    list_filter = ('gender',)
    list_display_links = ('phone', 'national_code', 'first_name', 'last_name', 'email',)
    list_editable = ('gender',)
    ordering = ('first_name', 'last_name', 'phone', 'email', 'national_code', 'gender')


admin.site.register(Customer, CustomerAdmin)


class AddressAdmin(admin.ModelAdmin):
    form = AddressForm
    list_display = ('title', 'owner', 'city', 'post_code')
    list_filter = ('title', 'owner', 'city')
    list_display_links = ('owner', 'city' )
    list_editable = ('title', 'post_code')
    ordering = ('title', 'owner', 'city', 'post_code')


admin.site.register(Address, AddressAdmin)


def logical_delete(modeladmin, request, queryset):
    queryset.update(deleted=True)


admin.site.add_action(logical_delete)