from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError


from django.utils import timezone 
from django.db import transaction

from .models import Product, Promotion, Order
from .serializers import ProductSerializer, PromotionSerializer, OrderSerializer


class ProductPagination(PageNumberPagination):
    page_size = 5 
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
            products = Product.objects.all()
            paginator = ProductPagination()
            result_page = paginator.paginate_queryset(products, request)
            serializer = ProductSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Product added successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class UpdateProduct(APIView):
    permission_classes = [IsAdminUser] 

    def patch(self, request, id, *args, **kwargs):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Product updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PromotionPagination(PageNumberPagination):
    page_size = 5 
    page_size_query_param = 'page_size'
    max_page_size = 100

class PromotionView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        now = timezone.now()
        print(now) 
        promotions = Promotion.objects.filter(start_date__lte=now, end_date__gte=now)

        paginator = PromotionPagination()
        result_page = paginator.paginate_queryset(promotions, request)
        serializer = PromotionSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PromotionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Promotion added successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdatePromotion(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id, *args, **kwargs):
        try:
            promotion = Promotion.objects.get(id=id)
        except Promotion.DoesNotExist:
            return Response({"detail": "Promotion not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PromotionSerializer(promotion, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Promotion updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class OrderView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            try:
                return self.create_order(request,serializer.validated_data)
            except ValidationError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def price_after_max_deduction(self, product): 
        now = timezone.now()
        applicable_promotions = product.promotions.filter(
            start_date__lte=now, 
            end_date__gte=now,
        )
        product_price = product.price
        best_deduction = 0 
        for promo in applicable_promotions:
            type = promo.discount_type 
            value = promo.value

            if type == 'fixed':
                deduction = value
            elif type == 'percentage':
                deduction = (product_price * value / 100)

            best_deduction = max(best_deduction, deduction) 
        return best_deduction

    def create_order(self, request, validated_data):
        items = validated_data['items']
        total_price = 0

        with transaction.atomic():
            for item in items:
                product = Product.objects.select_for_update().get(id=item['product_id'])
                product.stock -= item['quantity']
                product.save()
                max_deduction = self.price_after_max_deduction(product)
                total_price += min(product.price - max_deduction, 0) * item['quantity']
            
            order = Order.objects.create(
                user_id=request.user,
                items=items,
                total_price=total_price,
            )
        
        return Response({
            'message': 'Order placed successfully.',
            'data': OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs): 
        orders = Order.objects.filter(user_id=request.user)
        
        paginator = OrderPagination()
        result_page = paginator.paginate_queryset(orders, request)
        
        serializer = OrderSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)