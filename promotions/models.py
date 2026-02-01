# promotions/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel, UUIDModel




class Coupon(TimeStampedModel, UUIDModel):
    """
    Discount coupons.
    """
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)

    DISCOUNT_TYPES = [
        ('percentage', _('Percentage')),
        ('fixed', _('Fixed Amount')),
    ]

    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)

    min_purchase_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    max_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Maximum discount for percentage coupons"
    )

    usage_limit = models.IntegerField(
        null=True,
        blank=True,
        help_text="Total number of times coupon can be used"
    )
    usage_count = models.IntegerField(default=0)

    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'coupons'

    def __str__(self):
        return self.code

    def is_valid(self):
        """Check if coupon is currently valid"""
        from django.utils import timezone
        now = timezone.now()

        if not self.is_active:
            return False
        if now < self.valid_from or now > self.valid_to:
            return False
        if self.usage_limit and self.usage_count >= self.usage_limit:
            return False

        return True
