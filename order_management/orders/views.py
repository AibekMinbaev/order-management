from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination


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

