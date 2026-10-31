
from django import forms
from django.forms import inlineformset_factory

from .models import Sale, SaleItem
from products.models import Product


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = [
            "invoice_number",
            "customer",
            "paid_amount",
            "status",
            "notes",
        ]

        widgets = {
            "invoice_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "رقم الفاتورة",
            }),
            "customer": forms.Select(attrs={
                "class": "form-control",
            }),
            "paid_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0",
                "step": "0.01",
            }),
            "status": forms.Select(attrs={
                "class": "form-control",
            }),
            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "ملاحظات إضافية",
            }),
        }


class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = [
            "product",
            "quantity",
            "unit_price",
        ]

        widgets = {
            "product": forms.Select(attrs={
                "class": "form-control",
            }),
            "quantity": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "1",
                "step": "1",
            }),
            "unit_price": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0",
                "step": "0.01",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        active_products = Product.objects.filter(is_active=True)

        # السماح باختيار المنتجات النشطة فقط،
        # مع إبقاء المنتج الحالي عند تعديل عنصر قديم.
        if self.instance.pk and self.instance.product_id:
            active_products = Product.objects.filter(
                pk__in=active_products.values("pk")
            ) | Product.objects.filter(
                pk=self.instance.product_id
            )

        self.fields["product"].queryset = active_products.distinct()

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]

        if quantity < 1:
            raise forms.ValidationError(
                "يجب أن تكون الكمية أكبر من صفر."
            )

        return quantity

    def clean_unit_price(self):
        price = self.cleaned_data["unit_price"]

        if price < 0:
            raise forms.ValidationError(
                "لا يمكن أن يكون سعر الوحدة سالبًا."
            )

        return price


SaleItemFormSet = inlineformset_factory(
    Sale,
    SaleItem,
    form=SaleItemForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)