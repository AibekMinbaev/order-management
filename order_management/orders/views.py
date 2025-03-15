from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


from django.utils import timezone 

from .models import Product, Promotion
from .serializers import ProductSerializer, PromotionSerializer


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
