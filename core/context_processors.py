# core/context_processors.py


from django.db.models import Sum

from cart.views import CartMixin


def cart_item_count(request):
    helper = CartMixin()
    try:
        cart = helper._get_or_create_cart(request)
        return {
            "cart_item_count": cart.items.aggregate(total=Sum("quantity"))["total"] or 0
        }
    except Exception:
        return {"cart_item_count": 0}
