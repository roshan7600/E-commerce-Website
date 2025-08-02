from django.contrib import admin
from .models import Category, Customer, Product, Order, CartItem, OrderGroup, OrderItem, Review

# Inline view of OrderItem inside OrderGroup admin panel
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

# Admin customization for OrderGroup
class OrderGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'total_price', 'is_paid']
    inlines = [OrderItemInline]

# Register your models here
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)        # This is your old single-item order model
admin.site.register(CartItem)
admin.site.register(OrderGroup, OrderGroupAdmin)

from .models import Wishlist  # ✅ Make sure this import is added

admin.site.register(Wishlist)
admin.site.register(Review)

