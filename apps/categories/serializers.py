from rest_framework import serializers
from apps.categories.models import Category


class CategoryChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'lft', 'rgt')


class CategorySerializer(serializers.ModelSerializer):
    children = CategoryChildSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'lft', 'rgt', 'children')
        read_only_fields = ('lft', 'rgt')


class CategoryCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    parent_id = serializers.IntegerField(required=False, allow_null=True)


class CategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'parent', 'lft', 'rgt')
        read_only_fields = ('parent', 'lft', 'rgt')