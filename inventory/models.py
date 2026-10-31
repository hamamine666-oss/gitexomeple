from django.db import models
from products.models import Product


class Inventory(models.Model):

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="inventory",
        verbose_name="المنتج"
    )

    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="الكمية الحالية"
    )

    minimum_stock = models.PositiveIntegerField(
        default=5,
        verbose_name="الحد الأدنى للمخزون"
    )

    location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="موقع التخزين"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات"
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "مخزون"
        verbose_name_plural = "المخزون"
        ordering = ["product__name"]

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    @property
    def is_low_stock(self):
        return self.quantity <= self.minimum_stock