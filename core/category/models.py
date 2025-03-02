from django.db import models

from base.models import BaseModel


# Create your models here.
class Category(BaseModel):
    category_name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=500, null=True)
    parent = models.ForeignKey(
        "self", null=True, on_delete=models.CASCADE, related_name="sub_categories"
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name
