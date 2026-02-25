from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models, transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView

from products.models import Product, ProductVariant

from .models import Cart, CartItem

User = get_user_model()


class CartMixin:
    """
    Helper mixin to fetch or create the current cart.
    - Auth users: user-based cart
    - Guests: session-based cart
    """

    def _get_or_create_cart(self, request):
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
            return cart

        # Guest cart
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key

        cart, _ = Cart.objects.get_or_create(
            session_key=session_key, user=None, is_active=True
        )
        return cart


class CartDetailView(CartMixin, DetailView):
    model = Cart
    template_name = "cart/cart_detail.html"
    context_object_name = "cart"

    def get_object(self, queryset=None):
        return self._get_or_create_cart(self.request)

    def get(self, request, *args, **kwargs):
        cart = self.get_object()

        if not cart.items.exists():
            return redirect("products:product_list")

        self.object = cart
        context = self.get_context_data()
        return self.render_to_response(context)


class AddToCartView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        cart = self._get_or_create_cart(request)

        product_id = request.POST.get("product_id")
        variant_id = request.POST.get("variant_id")
        quantity = int(request.POST.get("quantity", 1))

        if not product_id:
            return JsonResponse({"error": "product_id is required"}, status=400)

        if quantity <= 0:
            return JsonResponse({"error": "quantity must be >= 1"}, status=400)

        product = get_object_or_404(Product, id=product_id)
        variant = None

        if variant_id:
            variant = get_object_or_404(ProductVariant, id=variant_id, product=product)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={"quantity": quantity},
        )

        if not created:
            item.quantity += quantity

        item.save()

        total_qty = cart.items.aggregate(total=models.Sum("quantity"))["total"] or 0

        return JsonResponse(
            {
                "message": "Item added to cart",
                "item_id": str(item.id),
                "item_quantity": item.quantity,
                "cart_total_qty": total_qty,
            },
            status=200,
        )


class UpdateCartItemView(CartMixin, View):
    """
    Bulk update cart quantities

    """

    def post(self, request, *args, **kwargs):
        cart = self._get_or_create_cart(request)

        updated = 0

        for key, value in request.POST.items():
            if key.startswith("quantities[") and key.endswith("]"):
                item_id = key[len("quantities[") : -1]

                try:
                    quantity = int(value)
                except (TypeError, ValueError):
                    continue

                if quantity < 1:
                    continue

                item = get_object_or_404(CartItem, id=item_id, cart=cart)
                item.quantity = quantity
                item.save()
                updated += 1

        return redirect("cart:detail")


class RemoveCartItemView(CartMixin, View):
    """
    Remove an item from cart.
    POST params:
        - item_id (required)
    """

    def post(self, request, *args, **kwargs):
        cart = self._get_or_create_cart(request)
        item_id = request.POST.get("item_id")

        if not item_id:
            return JsonResponse({"error": "item_id is required"}, status=400)

        item = get_object_or_404(CartItem, id=item_id, cart=cart)
        item.delete()

        return redirect("products:product_list")


class ClearCartView(CartMixin, View):
    """
    Clear all items from the current cart.
    """

    def post(self, request, *args, **kwargs):
        cart = self._get_or_create_cart(request)
        cart.items.all().delete()

        return redirect("products:product_list")


class MergeGuestCartView(LoginRequiredMixin, View):
    """
    Merge guest cart into user cart after login.
    Call this after login if you want to combine carts.
    """

    def post(self, request, *args, **kwargs):
        if not request.session.session_key:
            return JsonResponse({"message": "No guest cart to merge"}, status=200)

        session_key = request.session.session_key

        try:
            guest_cart = Cart.objects.get(
                session_key=session_key, user=None, is_active=True
            )
        except Cart.DoesNotExist:
            return JsonResponse({"message": "No guest cart to merge"}, status=200)

        user_cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)

        with transaction.atomic():
            for item in guest_cart.items.all():
                merged_item, created = CartItem.objects.get_or_create(
                    cart=user_cart,
                    product=item.product,
                    variant=item.variant,
                    defaults={"quantity": item.quantity},
                )
                if not created:
                    merged_item.quantity += item.quantity
                    merged_item.save()

            guest_cart.items.all().delete()
            guest_cart.is_active = False
            guest_cart.save()

        return JsonResponse({"message": "Guest cart merged into user cart"}, status=200)
