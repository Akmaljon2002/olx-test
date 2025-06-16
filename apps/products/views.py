from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.categories.models import Category
from apps.products.models import Product
from apps.products.schemas import product_by_category, product_detail_schema
from apps.products.serializers import ProductSerializer


class ProductByCategoryApiView(APIView):
    permission_classes = [AllowAny]

    @product_by_category
    def get(self, request, category_id):
        try:
            category = Category.objects.only('lft', 'rgt').get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=404)

        try:
            limit = min(int(request.GET.get('limit', 10)), 100)
            offset = max(int(request.GET.get('offset', 0)), 0)
        except ValueError:
            limit = 10
            offset = 0

        products_qs = Product.objects.filter(
            category__lft__gte=category.lft,
            category__rgt__lte=category.rgt
        ).values('id', 'title', 'price', 'description', 'category_id')[offset:offset + limit]

        return Response({
            "limit": limit,
            "offset": offset,
            "results": list(products_qs)
        })

@product_detail_schema
class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return get_object_or_404(
            Product.objects.only("id", "title", "price", "description", "category_id"),
            pk=self.kwargs['pk']
        )