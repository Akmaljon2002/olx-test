from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.categories.views import CategoryViewSet, CategoryCreateApiView, TaskStatusApiView, CategoryUpdateAPIView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('create/', CategoryCreateApiView.as_view(), name='category-create'),
    path('update/<int:pk>/', CategoryUpdateAPIView.as_view(), name='category-update'),

    path("tasks/<str:task_id>/status/", TaskStatusApiView.as_view()),
]
