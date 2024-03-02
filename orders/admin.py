from django.contrib import admin
from orders.models import Order, OrderItem,UserPayment

# Register your models here.

class UserPaymentAdmin(admin.ModelAdmin):
    model = UserPayment


class OrderItemAdmin(admin.StackedInline):
    model = OrderItem
    raw_id_fields = ["product"]



class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ["first_name","last_name",
               "postal_code","adress",
                "email","city",
                "created_at","paid"]
    list_filter = ["created_at","updated_at","paid"]
    inlines = [OrderItemAdmin]





admin.site.register(Order, OrderAdmin)
admin.site.register(UserPayment, UserPaymentAdmin)

