from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BulkUploadAPIView, ProductViewSet

router = DefaultRouter()
router.register(r"", ProductViewSet, basename="products")

urlpatterns = [
    path("upload/", BulkUploadAPIView.as_view(), name="upload"),
    path("", include(router.urls)),
]
