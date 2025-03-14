from django.shortcuts import render

from rest_framework import status 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication 
from .serializers import UserRegistrationSerializer


class RegisterUser(APIView):
    permission_classes = [AllowAny] 

    def post(self, request, *args, **kwargs): 
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid(): 
            user = serializer.save() 
            return Response({
                'message': 'User registered successfully', 
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
