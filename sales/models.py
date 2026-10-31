from django.db import models
from products.models import Product
from customers.models import Customer



class Sale(models.Model):

    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="رقم الفاتورة"
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="sales",
        verbose_name="العميل"
    )

    sale_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ البيع"
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="الإجمالي"
    )

    paid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="المبلغ المدفوع"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات"
    )

    STATUS_CHOICES = [
        ("paid", "مدفوعة"),
        ("pending", "معلقة"),
        ("partial", "مدفوعة جزئياً"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="الحالة"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "فاتورة بيع"
        verbose_name_plural = "فواتير المبيعات"
        ordering = ["-sale_date"]

    def __str__(self):
        return self.invoice_number


class SaleItem(models.Model):

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="الفاتورة"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="sale_items",
        verbose_name="المنتج"
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="الكمية"
    )

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="سعر الوحدة"
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="الإجمالي"
    )

    class Meta:
        verbose_name = "تفصيل البيع"
        verbose_name_plural = "تفاصيل المبيعات"

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"