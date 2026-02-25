from django.contrib import admin

from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    autocomplete_fields = ["product", "variant"]

    def subtotal_display(self, obj):
        return obj.subtotal

    subtotal_display.short_description = "Subtotal"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "session_key", "is_active"]
    search_fields = ["session_key", "user"]
    list_filter = ["is_active"]
    empty_value_display = "-empty-"
    inlines = [CartItemInline]
