from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.categories.serializers import CategorySerializer, CategoryCreateSerializer, CategoryUpdateSerializer

category_viewset_schema = extend_schema_view(
    list=extend_schema(
        tags=["Categories"],
        operation_id="List All Categories",
        description="All categories are returned in a tree structure.",
        responses={200: CategorySerializer(many=True)},
    ),
    retrieve=extend_schema(
        tags=["Categories"],
        operation_id="Retrieve Single Category",
        description="Returns a single category by its ID.",
        responses={200: CategorySerializer},
    ),
)

category_create_schema = extend_schema(
        tags=['Categories'],
        operation_id='Create Category',
        request=CategoryCreateSerializer,
        responses={
            201: CategorySerializer
        }
    )


category_update_schema = extend_schema(
    tags=["Categories"],
    operation_id="Update Category",
    description="Updates an existing category by its ID.",
    responses={
        200: CategoryUpdateSerializer,
        404: "Category not found.",
        400: "Bad request."
    }
)

