from django.contrib import admin

from .models import Brand, Category, Product, ProductImage, ProductVariant


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    empty_value_display = "-empty-"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent", "is_active"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]
    empty_value_display = "-empty-"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ["image", "alt_text", "is_primary", "display_order"]
    ordering = ["display_order"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "sku",
        "brand",
        "category",
        "stock_quantity",
        "is_available",
    ]
    list_filter = ["is_available", "brand", "category"]
    list_editable = ["is_available"]
    search_fields = ["name", "sku"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]
    empty_value_display = "-empty-"


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ["name", "sku", "final_price", "stock_quantity", "product"]
    list_filter = ["product", "stock_quantity"]
    search_fields = ["name", "sku"]
    empty_value_display = "-empty-"
