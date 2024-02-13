from django.contrib import admin
from django.contrib.admin import ModelAdmin, register

from payment.models import ShippingAddress, Order, OrderItem

# Register your models here.
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('id', 'user', 'shipping_address', 'amount', 'created', 'updated', 'paid')
    list_filter = ['created', 'updated', 'paid']
    search_fields = ['user__username']


