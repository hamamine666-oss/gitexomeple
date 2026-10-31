from django.db import models


class Supplier(models.Model):

    name = models.CharField(
        max_length=200,
        verbose_name="اسم المورد"
    )

    company_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="اسم الشركة"
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="الهاتف"
    )

    email = models.EmailField(
        blank=True,
        verbose_name="البريد الإلكتروني"
    )

    address = models.TextField(
        blank=True,
        verbose_name="العنوان"
    )

    tax_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="الرقم الضريبي"
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="الرصيد"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات"
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

    class Meta:
        verbose_name = "مورد"
        verbose_name_plural = "الموردون"
        ordering = ["name"]

    def __str__(self):
        return self.name