from django.contrib import admin
from .models import ShippingAddress, Order,OrderItem
from django.contrib.auth.models import User

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# Create an order item inline
class OrderItemInline(admin.StackedInline):
    model=OrderItem
    # removing empty extra order items
    extra = 0 

# Extend our order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields =["date_ordered"] # show date
    fields = ["user","full_name","email","shipping_address","amount_paid","date_ordered","shipped","date_shipped"]
    inlines = [OrderItemInline]

# unregister order model
admin.site.unregister(Order)

# Re-register order model with extended fields
admin.site.register(Order, OrderAdmin)  