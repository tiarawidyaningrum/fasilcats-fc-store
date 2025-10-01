from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'price', 'category', 'is_featured', 'stock']
    list_filter = ['user', 'category', 'is_featured']
    search_fields = ['name', 'brand']