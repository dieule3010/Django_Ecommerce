from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
class OrderItemInline(admin.StackedInline):
  model = OrderItem
class OrderAdmin(admin.ModelAdmin):
  model = Order
  inlines = [OrderItemInline]
# Unregister Order Model
admin.site.unregister(Order)
#Re-register
admin.site.register(Order, OrderAdmin)
