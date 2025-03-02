from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        include(
            [
                path("auth/", include("core.custom_auth.urls")),
                path("category/", include("core.category.urls")),
                path("product/", include("core.product.urls")),
            ]
        ),
    ),
]
