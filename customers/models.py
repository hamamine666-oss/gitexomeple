from django.db import models


class Customer(models.Model):

    name = models.CharField(
        max_length=200,
        verbose_name="اسم العميل"
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

    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات"
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="الرصيد"
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
        verbose_name = "عميل"
        verbose_name_plural = "العملاء"
        ordering = ["name"]

    def __str__(self):
        return self.name
