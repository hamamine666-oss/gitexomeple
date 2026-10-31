
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, F

from .models import Inventory
from products.models import Product


def inventory_list(request):
    # جلب سجلات المخزون مع بيانات المنتجات
    inventories = Inventory.objects.select_related("product").all()

    # البحث باسم المنتج أو رمزه
    search = request.GET.get("search", "").strip()

    if search:
        inventories = inventories.filter(
            Q(product__name__icontains=search) |
            Q(product__code__icontains=search)
        )

    # حساب عدد السجلات التي وصلت إلى الحد الأدنى أو أقل
    low_stock_count = inventories.filter(
        quantity__lte=F("minimum_stock")
    ).count()

    context = {
        "inventories": inventories,
        "search": search,
        "low_stock_count": low_stock_count,
    }

    return render(request, "inventory/list.html", context)


def inventory_create(request):
    products = Product.objects.filter(is_active=True)

    if request.method == "POST":
        product_id = request.POST.get("product")
        quantity = request.POST.get("quantity") or "0"
        minimum_stock = request.POST.get("minimum_stock") or "5"
        location = request.POST.get("location", "").strip()
        notes = request.POST.get("notes", "").strip()

        # التحقق من اختيار المنتج
        if not product_id:
            messages.error(request, "يرجى اختيار المنتج.")
            return render(
                request,
                "inventory/form.html",
                {"products": products},
            )

        product = get_object_or_404(
            Product,
            pk=product_id,
            is_active=True,
        )

        # التحقق من صحة الكميات
        try:
            quantity = int(quantity)
            minimum_stock = int(minimum_stock)

            if quantity < 0 or minimum_stock < 0:
                raise ValueError

        except (ValueError, TypeError):
            messages.error(
                request,
                "يرجى إدخال كميات صحيحة، ولا يمكن أن تكون سالبة.",
            )
            return render(
                request,
                "inventory/form.html",
                {"products": products},
            )

        Inventory.objects.create(
            product=product,
            quantity=quantity,
            minimum_stock=minimum_stock,
            location=location,
            notes=notes,
        )

        messages.success(request, "تمت إضافة سجل المخزون بنجاح.")
        return redirect("inventory:list")

    return render(
        request,
        "inventory/form.html",
        {"products": products},
    )


def inventory_edit(request, pk):
    inventory = get_object_or_404(
        Inventory.objects.select_related("product"),
        pk=pk,
    )

    products = Product.objects.filter(is_active=True)

    # إبقاء المنتج الحالي متاحًا حتى إن أصبح غير نشط
    if not inventory.product.is_active:
        products = (products | Product.objects.filter(
            pk=inventory.product_id
        )).distinct()

    if request.method == "POST":
        product_id = request.POST.get("product")
        quantity = request.POST.get("quantity") or "0"
        minimum_stock = request.POST.get("minimum_stock") or "5"
        location = request.POST.get("location", "").strip()
        notes = request.POST.get("notes", "").strip()

        if not product_id:
            messages.error(request, "يرجى اختيار المنتج.")
            return render(
                request,
                "inventory/form.html",
                {"inventory": inventory, "products": products},
            )

        product = get_object_or_404(
            products,
            pk=product_id,
        )

        try:
            quantity = int(quantity)
            minimum_stock = int(minimum_stock)

            if quantity < 0 or minimum_stock < 0:
                raise ValueError

        except (ValueError, TypeError):
            messages.error(
                request,
                "يرجى إدخال كميات صحيحة، ولا يمكن أن تكون سالبة.",
            )
            return render(
                request,
                "inventory/form.html",
                {"inventory": inventory, "products": products},
            )

        inventory.product = product
        inventory.quantity = quantity
        inventory.minimum_stock = minimum_stock
        inventory.location = location
        inventory.notes = notes

        inventory.save()

        messages.success(request, "تم تعديل سجل المخزون بنجاح.")
        return redirect("inventory:list")

    return render(
        request,
        "inventory/form.html",
        {
            "inventory": inventory,
            "products": products,
        },
    )


def inventory_delete(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)

    if request.method == "POST":
        inventory.delete()
        messages.success(request, "تم حذف سجل المخزون بنجاح.")

    return redirect("inventory:list")