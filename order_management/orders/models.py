from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User  
from django.utils import timezone
from django.core.exceptions import ValidationError


from enum import Enum 

# Create your models here.
class Product(models.Model): 
    name = models.CharField(max_length=200, null=False, blank=False) 
    price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)], null=False, blank=False)
    stock = models.PositiveIntegerField(null=False, blank=False)  

    def __str__(self): 
        return self.name 

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
    items = models.JSONField(null=False, blank=False)
    total_price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)], null=False, blank=False) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self): 
        return f"Order by {self.user_id}"

class Promotion(models.Model): 
    PERCENTAGE = "percentage"
    FIXED = "fixed"

    DISCOUNT_CHOICES = [
        (PERCENTAGE,"Percentage"),
        (FIXED,"Fixed"),
    ]

    name = models.CharField(max_length=200, null=False, blank=False) 
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_CHOICES, null=False, blank=False) 
    value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)], null=False, blank=False)  
    start_date = models.DateTimeField(null=False, blank=False) 
    end_date = models.DateTimeField(null=False, blank=False) 
    applicable_products = models.ManyToManyField(Product, related_name='promotions', blank=False)


    def __str__(self): 
        return self.name  

    def is_active(self): 
        return self.start_date <= timezone.now().date() <= self.end_date 
    
    # validation when editing on django admin, django shell 
    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError({
                'end_date': "End date cannot be before the start date."
            })

        if self.discount_type == self.PERCENTAGE and self.value > 100:
            raise ValidationError({'value': ("Percentage discount cannot exceed 100%")})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)