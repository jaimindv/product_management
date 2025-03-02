from django.db import models

from base.models import BaseModel
from core.category.models import Category

from .utils import get_product_photo_random_filename


# Create your models here.
class Product(BaseModel):
    product_name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL, related_name="product"
    )
    product_description = models.CharField(max_length=500)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    stock_quantity = models.PositiveIntegerField()
    sku = models.CharField(max_length=50, unique=True)
    image = models.ImageField(
        upload_to=get_product_photo_random_filename,
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.product_name
