from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User  
from django.utils import timezone

from enum import Enum 

# Create your models here.
class Product(models.Model): 
    name = models.CharField(max_length=200, null=False, blank=False) 
    price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)], null=False, blank=False)
    stock = models.PositiveIntegerField(null=False, blank=False)  

    def __str__(self): 
        return self.name 

class OrderItem(models.Model): 
    order = models.ForeignKey('Order', on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING) 
    product_name = models.CharField(max_length=200, null=False, blank=False) # if product is deleted
    product_price = models.PositiveIntegerField(null=False, blank=False) # price at the order time (if price changes)
    quantity = models.PositiveIntegerField(null=False, blank=False) 

    def save(self, *args, **kwargs): 
        self.product_name = self.product.name 
        self.product_price = self.product.price 
        
        super().save(*args, **kwargs) 
    

class Order(models.Model): 
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False) 
    total_price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)], null=False, blank=False) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self): 
        return f"Order by {self.user_id}"

class Promotion(models.Model): 
    PERCENTAGE = "percentage"
    FIXED = "fixed"

    DISCOUNT_CHOICES = {
        PERCENTAGE:"Percentage",
        FIXED:"Fixed"
    }

    name = models.CharField(max_length=200, null=False, blank=False) 
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_CHOICES, default=PERCENTAGE, null=False, blank=False) 
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=False, blank=False)  
    start_date = models.DateTimeField(null=False, blank=False) 
    end_date = models.DateTimeField(null=False, blank=False) 
    applicable_products = models.ManyToManyField(Product, related_name='promotions', blank=False)


    def __str__(self): 
        return self.name  

    def is_active(self): 
        return self.start_date <= timezone.now().date() <= self.end_date 