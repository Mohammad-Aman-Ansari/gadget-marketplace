from django.contrib import admin
from .models import Category, Gadget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Gadget)
class GadgetAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'category', 'condition', 'price', 'stock', 'seller')
    list_filter = ('condition', 'category', 'brand')
    search_fields = ('title', 'brand', 'description')
