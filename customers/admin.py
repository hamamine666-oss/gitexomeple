from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "email", "balance", "is_active", "created_at")
    search_fields = ("name", "phone", "email")
    list_filter = ("is_active", "created_at")
    list_display_links = ("id", "name")
    list_editable = ("is_active",)
    ordering = ("name",)
    list_per_page = 25
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("معلومات العميل", {"fields": ("name", "phone", "email")}),
        ("العنوان والملاحظات", {"fields": ("address", "notes")}),
        ("المعلومات المالية", {"fields": ("balance",)}),
        ("حالة العميل", {"fields": ("is_active",)}),
        ("التواريخ", {"fields": ("created_at", "updated_at")}),
    )