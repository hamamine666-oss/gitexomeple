from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="اسم الفئة"
    )

    description = models.TextField(
        blank=True,
        verbose_name="الوصف"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="نشطة"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "فئة"
        verbose_name_plural = "الفئات"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="كود المنتج"
    )

    name = models.CharField(
        max_length=200,
        verbose_name="اسم المنتج"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="الفئة"
    )

    description = models.TextField(
        blank=True,
        verbose_name="الوصف"
    )

    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="سعر الشراء"
    )

    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="سعر البيع"
    )

    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=19,
        verbose_name="نسبة الضريبة %"
    )

    minimum_stock = models.PositiveIntegerField(
        default=5,
        verbose_name="الحد الأدنى للمخزون"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    stock_quantity = models.PositiveIntegerField(
    default=0,
    verbose_name="الكمية المتوفرة")
    
    class Meta:
        verbose_name = "منتج"
        verbose_name_plural = "المنتجات"
        ordering = ["name"]

    def __str__(self):
        return f"{self.code} - {self.name}"
