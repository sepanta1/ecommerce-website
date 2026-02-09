# products/models.py

from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from core.models import TimeStampedModel, UUIDModel, SoftDeleteModel


class Category(TimeStampedModel, UUIDModel):
    """
    Product category with hierarchical structure.
    Self-referencing FK for nested categories.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(TimeStampedModel, UUIDModel):
    """
    Separate brand entity - following normalization (avoid duplication).
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'brands'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(TimeStampedModel, UUIDModel, SoftDeleteModel):
    """
    Main product model following normalization principles.
    Uses mixins for timestamp, UUID, and soft delete functionality.
    """
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    description = models.TextField()
    sku = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        help_text="SKU for simple products without variants"
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name='products',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )

    # Pricing - stored in smallest currency unit (cents) to avoid float issues
    # price ==> selling price!
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    # The amount it costs YOU to acquire or produce the product.
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Cost to acquire product"
    )

    # Inventory
    stock_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    is_available = models.BooleanField(default=True)

    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created']
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return self.name

    @property
    def profit_margin(self):
        """
        Calculate profit margin percentage.
        Property field for computed values.
        """
        if self.price and self.cost_price:
            profit = self.price - self.cost_price
            return (profit / self.price) * 100
        return 0

    @property
    def is_in_stock(self):
        """Check if product has stock"""
        return self.stock_quantity > 0 and self.is_available and not self.is_deleted


class ProductImage(TimeStampedModel, UUIDModel):
    """
    Separate table for product images (1-to-many).
    Normalized - avoids storing multiple images in single field.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/%Y/%m/',default= 'products/default.jpg')
    alt_text = models.CharField(max_length=200)
    is_primary = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)

    class Meta:
        db_table = 'product_images'
        ordering = ['display_order', 'created']
        constraints = [
            models.UniqueConstraint(
                fields=['product'],
                condition=models.Q(is_primary=True),
                name='unique_primary_image_per_product'
            )
        ]
    def __str__(self):
        return f"{self.product.name} - Image {self.display_order}"


class ProductVariant(TimeStampedModel, UUIDModel):
    """
    For products with variations (size, color, etc.).
    Following normalization - separate table for variants.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )
    name = models.CharField(max_length=100)  # e.g., "Large, Red"
    sku = models.CharField(max_length=50, unique=True)

    # Variant-specific pricing and stock
    price_adjustment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Price difference from base product"
    )
    stock_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        db_table = 'product_variants'

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    @property
    def final_price(self):
        """Calculate final price including adjustment"""
        return self.product.price + self.price_adjustment
