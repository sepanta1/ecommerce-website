# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel, UUIDModel

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Allows for future customization without migration headaches.
    """
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email


class CustomerProfile(TimeStampedModel):
    """
    One-to-one relationship with User for customer-specific data.
    Keeps auth-related and business logic separated (Single Responsibility).
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )
    date_of_birth = models.DateField(null=True, blank=True)
    loyalty_points = models.IntegerField(default=0)
    preferred_payment_method = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'customer_profiles'
    
    def __str__(self):
        return f"Profile: {self.user.email}"
    
class Address(TimeStampedModel, UUIDModel):
    """
    Normalized address table.
    Allows multiple addresses per user.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'addresses'
        verbose_name_plural = 'Addresses'
    
    def __str__(self):
        return f"{self.full_name} - {self.address_type}"

