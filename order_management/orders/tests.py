from django.test import TestCase
from django.db import connection
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status 
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta

import pytest 

from .models import Product, Promotion, Order 


def authenticate(user):
    refresh = RefreshToken.for_user(user) 
    access_token = str(refresh.access_token) 

    client = APIClient() 
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    return client 

@pytest.fixture 
def authenticated_admin_user(): 
    user = User.objects.create_user(username="user", password="user123", is_staff=True)  
    client = authenticate(user)
    return user, client

@pytest.fixture 
def authenticated_user(): 
    user = User.objects.create_user(username="user", password="user123")  
    client = authenticate(user) 
    return user, client


@pytest.mark.django_db
def test_database_connection():
    try:
        connection.ensure_connection()
        assert connection.is_usable() is True
    except Exception:
        assert False, "Database connection failed!"


@pytest.mark.django_db 
def test_product_creation_as_admin(authenticated_admin_user): 
    admin_user, client = authenticated_admin_user

    product_data = {
        "name": "water", 
        "price":120, 
        "stock":10
    } 

    response = client.post("/products/", product_data, format="json") 
    assert response.status_code == status.HTTP_201_CREATED
    assert Product.objects.count() == 1
    assert Product.objects.first().name == "water" 

@pytest.mark.django_db 
def test_product_creation_as_not_admin(authenticated_user): 
    user, client = authenticated_user
    
    product_data = {
        "name": "water", 
        "price":120, 
        "stock":10
    } 

    response = client.post("/products/", product_data, format="json") 
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Product.objects.count() == 0

@pytest.mark.django_db 
def test_invalid_product_creation_as_admin(authenticated_admin_user): 
    admin_user, client = authenticated_admin_user

    product_data = {
        "name": "water", 
        "price":120, 
        "stock":-1
    } 

    response = client.post("/products/", product_data, format="json") 
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Product.objects.count() == 0


@pytest.mark.django_db 
def test_promotion_creation_as_admin(authenticated_admin_user): 
    admin, client = authenticated_admin_user  

    product = Product.objects.create(name="product_1", price=200, stock=2)

    promotion_data = {
        "name": "black friday", 
        "discount_type": "fixed", 
        "value": 100, 
        "start_date": (now() + timedelta(days=1)).isoformat(), 
        "end_date": (now() + timedelta(days=2)).isoformat(), 
        "applicable_products": [product.id]
    }

    response = client.post("/promotions/", data=promotion_data, format="json") 

    assert response.status_code == status.HTTP_201_CREATED
    assert Promotion.objects.count() == 1
    assert Promotion.objects.first().name == "black friday"

@pytest.mark.django_db 
def test_invalid_promotion_creation_as_admin(authenticated_admin_user): 
    admin, client = authenticated_admin_user  

    product = Product.objects.create(name="product_1", price=200, stock=2)

    promotion_data = {
        "name": "black friday", 
        "discount_type": "percentage", 
        "value": 200, 
        "start_date": (now() + timedelta(days=1)).isoformat(), 
        "end_date": (now() + timedelta(days=2)).isoformat(), 
        "applicable_products": [product.id]
    }

    response = client.post("/promotions/", data=promotion_data, format="json") 

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {'value': ['Percentage discount cannot exceed 100% (API)']}

@pytest.mark.django_db 
def test_invalid_promotion_creation_as_admin(authenticated_admin_user): 
    admin, client = authenticated_admin_user  

    product = Product.objects.create(name="product_1", price=200, stock=2)

    promotion_data = {
        "name": "black friday", 
        "discount_type": "percentage", 
        "value": 100, 
        "start_date": (now() + timedelta(days=2)).isoformat(), 
        "end_date": (now() + timedelta(days=1)).isoformat(), 
        "applicable_products": [product.id]
    }

    response = client.post("/promotions/", data=promotion_data, format="json") 

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {'end_date': ["End date cannot be before the start date.(API)"]}
