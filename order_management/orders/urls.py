from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductView.as_view()),
    path('products/<int:id>/', views.UpdateProduct.as_view(), name='update_product'),
]
