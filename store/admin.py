from django.contrib import admin
from .models import *



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name',)
    search_fields=('name',)
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','quantity','price','discounted_price','category',)
    list_filter=('category',)
    search_fields=('name',)
    list_per_page=10

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=(
        "first_name",
        "middle_name",
        "last_name",
        "address",
        "gender",
    )
    search_fields=('first_name','user__email')
    list_per_page=10


class CartItemInline(admin.TabularInline):
    model = CartItem
    

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=('customer',)
    autocomplete_fields=('customer',)
    inlines=(CartItemInline,)
    




class OrderItemInline(admin.StackedInline):
    model = OrderItem
    
    
    


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=(
        "customer",
        "status",
        "payment_status",
        "shipping_address",
    )
    inlines=(OrderItemInline,)
    

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'cart']
    
    
admin.site.register(OrderItem)
admin.site.register(OrderSummary)