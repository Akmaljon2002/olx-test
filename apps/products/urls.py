from django.urls import path
from apps.products.views import ProductByCategoryApiView, ProductDetailAPIView

urlpatterns = [
    path('by-category/<int:category_id>/', ProductByCategoryApiView.as_view(), name='product-by-category'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
]