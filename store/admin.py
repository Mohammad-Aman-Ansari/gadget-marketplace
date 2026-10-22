from django.contrib import admin
from .models import Category, Gadget, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Gadget)
class GadgetAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'category', 'condition', 'price', 'stock', 'seller')
    list_filter = ('condition', 'category', 'brand')
    search_fields = ('title', 'brand', 'description')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'total_amount', 'shipping_address', 'created_at')
    inlines = [OrderItemInline]