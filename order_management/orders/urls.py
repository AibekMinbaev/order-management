from django.urls import path
from . import views

urlpatterns = [
    # Product endpoints
    path('products/', views.ProductView.as_view(), name='product_list_create'),
    path('products/<int:id>/', views.UpdateProduct.as_view(), name='update_product'),

    # Promotion endpoints
    path('promotions/', views.PromotionView.as_view(), name='promotion_list_create'),
    path('promotions/<int:id>/', views.UpdatePromotion.as_view(), name='update_promotion'),

    path('orders/', views.OrderView.as_view(), name='order_list_create'),
]
