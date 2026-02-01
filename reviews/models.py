# reviews/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel, UUIDModel
from products.models import Product
from django.conf import settings

class Review(TimeStampedModel, UUIDModel):
    """
    Product reviews.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'reviews'
        unique_together = ['product', 'user']
        ordering = ['-created']
    
    def __str__(self):
        return f"{self.product.name} - {self.rating}★"
    
