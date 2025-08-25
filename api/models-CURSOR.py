from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Vendor(models.Model):
    """Vendor/Supplier model"""

    name = models.CharField(max_length=200, unique=True)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Vendor"
        verbose_name_plural = "Vendors"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model"""

    CATEGORY_CHOICES = [
        ("electronics", "Electronics"),
        ("clothing", "Clothing"),
        ("books", "Books"),
        ("home", "Home & Garden"),
        ("sports", "Sports & Outdoors"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, unique=True, blank=True)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="other"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        blank=True,
        null=True,
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def profit_margin(self):
        """Calculate profit margin if cost price is available"""
        if self.cost_price:
            return ((self.price - self.cost_price) / self.price) * 100
        return None


class Member(models.Model):
    """Member/Customer model"""

    MEMBERSHIP_CHOICES = [
        ("basic", "Basic"),
        ("premium", "Premium"),
        ("vip", "VIP"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="member_profile"
    )
    membership_type = models.CharField(
        max_length=20, choices=MEMBERSHIP_CHOICES, default="basic"
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__username"]
        verbose_name = "Member"
        verbose_name_plural = "Members"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.membership_type})"


class Order(models.Model):
    """Order model"""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
        ("refunded", "Refunded"),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="orders")
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    shipping_address = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.order_number} - {self.member}"

    def save(self, *args, **kwargs):
        """Auto-generate order number if not provided"""
        if not self.order_number:
            # Generate order number: ORD-YYYYMMDD-XXXX
            from datetime import datetime

            date_str = datetime.now().strftime("%Y%m%d")
            last_order = (
                Order.objects.filter(order_number__startswith=f"ORD-{date_str}")
                .order_by("-order_number")
                .first()
            )

            if last_order:
                last_num = int(last_order.order_number.split("-")[-1])
                new_num = last_num + 1
            else:
                new_num = 1

            self.order_number = f"ORD-{date_str}-{new_num:04d}"

        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Order item model for order-product relationship"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return (
            f"{self.quantity}x {self.product.name} in Order {self.order.order_number}"
        )

    def save(self, *args, **kwargs):
        """Auto-calculate total price"""
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
