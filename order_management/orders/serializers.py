from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.db import transaction
from .models import Product, Promotion, Order 

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock']
        read_only_fields = ['id']


class PromotionSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Promotion
        fields = '__all__'

    def validate(self, data):
        instance = self.instance 
        start_date = data.get("start_date") 
        end_date = data.get("end_date") 

        if start_date is None: 
             start_date = instance.start_date 
        
        if end_date is None: 
             end_date = instance.start_date 

        if end_date < start_date:
            raise serializers.ValidationError({
                'end_date': "End date cannot be before the start date.(API)"
            })
                
        if data.get("discount_type") == Promotion.PERCENTAGE and data.get("value", 0) > 100:
            raise serializers.ValidationError({"value": "Percentage discount cannot exceed 100% (API)"})
        return data
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['items', 'status']

    def validate(self, data):
        items = data.get('items', [])
        for item in items:
            try: 
                product = Product.objects.get(id=item['product_id'])
            except Product.DoesNotExist:
                raise ValidationError(f"Product with ID {item['product_id']} does not exist.")

            if product.stock < item['quantity']:
                raise serializers.ValidationError(f"Not enough stock for product {product.name}")
        return data