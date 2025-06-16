from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from apps.products.serializers import ProductSerializer


product_by_category = extend_schema(
        tags=["Products"],
        operation_id="List Products by Category (including nested)",
        description="Retrieve all products in a category, including those in subcategories.",
        parameters=[
            OpenApiParameter(name='limit', type=OpenApiTypes.INT, required=False,
                             description='Count of products per page (default=10)'),
            OpenApiParameter(name='offset', type=OpenApiTypes.INT, required=False,
                             description='Offset for pagination (default=0)'),
        ],
        responses={200: ProductSerializer}
    )


product_detail_schema = extend_schema(
        tags=["Products"],
        operation_id="Retrieve, Update or Delete Product",
        description="Retrieve a single product by its ID, or update/delete it.",
        responses={
            200: ProductSerializer,
            404: "Product not found.",
            400: "Bad request."
        }
    )