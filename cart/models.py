# cart/models.py

from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel, UUIDModel
from products.models import Product, ProductVariant
from django.conf import settings

class Cart(TimeStampedModel, UUIDModel):
    """
    Shopping cart model.
    Session-based for guests, user-based for authenticated users.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='carts'
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'carts'
    
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.email}"
        return f"Guest cart {self.session_key}"


class CartItem(TimeStampedModel, UUIDModel):
    """
    Items in shopping cart.
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    
    class Meta:
        db_table = 'cart_items'
        unique_together = ['cart', 'product', 'variant']
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def subtotal(self):
        """Calculate cart item total"""
        price = self.variant.final_price if self.variant else self.product.price
        return price * self.quantity
