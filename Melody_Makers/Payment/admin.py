from django.contrib import admin
from .models import Order,OrderItem
from django.contrib.auth.models import User

admin.site.register(Order)
admin.site.register(OrderItem)

# create an orderItem Inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# Extend Order MOdel

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "amount_paid", "date_ordered"]
    inlines = [OrderItemInline]

admin.site.unregister(Order)
admin.site.register(Order,OrderAdmin)

