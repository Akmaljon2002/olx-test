from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.categories.models import Category
from apps.categories.schemas import category_viewset_schema, category_create_schema, category_update_schema
from apps.categories.serializers import CategorySerializer, CategoryCreateSerializer, CategoryUpdateSerializer
from apps.categories.tasks import create_category_task
from celery.result import AsyncResult
from core.celery import app


@category_viewset_schema
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.action == 'list':
            return Category.objects.filter(parent__isnull=True).only('id', 'name', 'parent', 'lft', 'rgt').prefetch_related('children')
        return Category.objects.only('id', 'name', 'parent', 'lft', 'rgt').prefetch_related('children')


class CategoryCreateApiView(APIView):
    permission_classes = [AllowAny]

    @category_create_schema
    def post(self, request):
        serializer = CategoryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data['name']
        parent_id = serializer.validated_data.get('parent_id')

        result = create_category_task.delay(name, parent_id)

        return Response({
            "message": "Category creation task queued",
            "task_id": result.id
        }, status=status.HTTP_202_ACCEPTED)


class TaskStatusApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, task_id):
        result = AsyncResult(task_id, app=app)

        return Response({
            "task_id": task_id,
            "status": result.status,
            "result": str(result.result)
        }, status=status.HTTP_200_OK)


@category_update_schema
class CategoryUpdateAPIView(UpdateAPIView):
    serializer_class = CategoryUpdateSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return get_object_or_404(
            Category.objects.only("id", "name", "parent_id", "lft", "rgt"),
            pk=self.kwargs['pk']
        )