import json

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from base.permissions import IsAdmin, IsAPIKeyAuthenticated
from core.category.models import Category

from .models import Product
from .serializers import ProductCreateUpdateSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action in ["list", "retrieve", "destroy"]:
            queryset = Product.objects.filter(is_deleted=False)

        return queryset.order_by("id")

    def get_serializer_class(self):
        actions = {
            "list": ProductSerializer,
            "create": ProductCreateUpdateSerializer,
            "update": ProductCreateUpdateSerializer,
            "partial_update": ProductSerializer,
            "retrieve": ProductSerializer,
        }
        if self.action in actions:
            self.serializer_class = actions.get(self.action)
        return super().get_serializer_class()

    def get_permissions(self):
        # Only Admins allowed to create/update/destroy categories
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [
                IsAPIKeyAuthenticated,
                IsAuthenticated,
                IsAdmin,
            ]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {
            "message": "Product created successfully.",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_data = {
            "message": "Product updated successfully.",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BulkUploadAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Read JSON file from request
            file = request.FILES.get("file")
            if not file:
                return Response(
                    {"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST
                )

            data = json.load(file)
            print("\n------------data: ", data)

            # Process Categories
            for category_data in data.get("categories", []):
                category, created = Category.objects.update_or_create(
                    category_name=category_data.get("category_name"),
                    defaults={
                        "description": category_data.get("description", ""),
                        "created_at": category_data.get("created_at", None),
                        "updated_at": category_data.get("updated_at", None),
                    },
                )

            # Process Products
            product_instances = []
            for product_data in data.get("products", []):
                category = Category.objects.filter(
                    category_name=product_data.get("category_name")
                ).first()
                if not category:
                    return Response(
                        {
                            "error": f"Category with name {product_data.get("category_name")} not found"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                product_instances.append(
                    Product(
                        category=category,
                        product_name=product_data["product_name"],
                        product_description=product_data.get("product_description", ""),
                        product_price=product_data["product_price"],
                        currency=product_data["currency"],
                        stock_quantity=product_data["stock_quantity"],
                        sku=product_data["sku"],
                        image=product_data["image_url"],
                        created_at=product_data.get("created_at", None),
                        updated_at=product_data.get("updated_at", None),
                    )
                )

            Product.objects.bulk_create(product_instances, ignore_conflicts=True)

            return Response(
                {"message": "Bulk upload successful"}, status=status.HTTP_201_CREATED
            )

        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
