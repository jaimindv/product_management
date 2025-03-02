from rest_framework import serializers

from core.category.serializers import CategorySerializer

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "category",
            "product_description",
            "product_price",
            "currency",
            "stock_quantity",
            "sku",
            "image",
            "created_at",
            "updated_at",
            "is_deleted",
        ]


class ProductCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "category",
            "product_description",
            "product_price",
            "currency",
            "stock_quantity",
            "sku",
            "image",
        ]
