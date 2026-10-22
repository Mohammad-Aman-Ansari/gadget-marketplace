from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Gadget(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Brand New'),
        ('like_new', 'Open Box / Like New'),
        ('refurbished', 'Certified Refurbished'),
        ('used', 'Pre-Owned / Good'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gadgets_for_sale')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='gadgets')
    title = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    description = models.TextField()
    image = models.ImageField(upload_to='gadgets/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_condition_display()}) - ₹{self.price}"

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    shipping_address = models.CharField(max_length=300)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.buyer.username} - ₹{self.total_amount}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    gadget = models.ForeignKey(Gadget, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.gadget.title}"