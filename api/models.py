from django.conf import settings
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(region="US")
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    admin = models.BooleanField(blank=True, default=False)
    vendor_mgr = models.BooleanField(blank=True, default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    STATUS_CHOICES = [
        ("reserved", "Reserved"),
        ("finalized", "Finalized"),
        ("vendor delivered", "Vendor Delivered"),
        ("distributed", "Distributed"),
        ("picked up", "Picked Up"),
        ("cancelled", "Cancelled"),
    ]
    PAYMENT_METHOD_CHOICES = [
        ("quickbooks invoice", "Quickbooks Invoice"),
    ]

    order_number = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="reserved"
    )
    payment_method = models.CharField(
        max_length=100, choices=PAYMENT_METHOD_CHOICES, default="quickbooks invoice"
    )
    payment_status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    STATUS_CHOICES = [
        ("available", "Available"),
        ("reserved", "Reserved"),
        ("finalized", "Finalized"),
        ("vendor delivered", "Vendor Delivered"),
        ("distributed", "Distributed"),
        ("picked up", "Picked Up"),
        ("cancelled", "Cancelled"),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shares_ordered = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_share = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="available"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
