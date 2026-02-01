from django.contrib import admin
from .models import Category,Brand ,Product, ProductImage, ProductVariant

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['name','sku','stock_quantity','is_available']
    empty_value_display = '-empty-'
    
