from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.permissions import IsAdmin, IsAPIKeyAuthenticated

from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action in ["list", "retrieve", "destroy"]:
            queryset = Category.objects.filter(is_deleted=False)

        return queryset.order_by("id")

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
            "message": "Category created successfully.",
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
            "message": "Category updated successfully.",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
