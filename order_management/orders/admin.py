from django.contrib import admin
from .models import Product, Order, OrderItem, Promotion

# Register your models here. 
admin.site.register(Product) 
admin.site.register(Promotion) 
