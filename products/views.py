
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.db.models import Q
from django.views.decorators.http import require_http_methods, require_POST

from .models import Product, Category


@login_required
@permission_required(
    "products.view_product",
    raise_exception=True,
)
def product_list(request):
    products = Product.objects.select_related(
        "category"
    ).all()

    search = request.GET.get("search", "").strip()

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search)
        )

    categories = Category.objects.filter(is_active=True)

    context = {
        "products": products,
        "categories": categories,
        "search": search,
    }

    return render(request, "products/list.html", context)


@login_required
@permission_required(
    "products.add_product",
    raise_exception=True,
)
@require_http_methods(["GET", "POST"])
def product_create(request):
    categories = Category.objects.filter(is_active=True)

    if request.method == "POST":
        code = (request.POST.get("code") or "").strip()
        name = (request.POST.get("name") or "").strip()
        category_id = request.POST.get("category")

        if not code or not name or not category_id:
            messages.error(
                request,
                "يرجى إدخال رمز المنتج واسمه واختيار الفئة."
            )
            return render(
                request,
                "products/form.html",
                {"categories": categories},
            )

        if Product.objects.filter(code=code).exists():
            messages.error(
                request,
                "رمز المنتج موجود مسبقًا! أدخل رمزًا آخر."
            )
            return render(
                request,
                "products/form.html",
                {"categories": categories},
            )

        category = get_object_or_404(
            categories,
            pk=category_id,
        )

        Product.objects.create(
            code=code,
            name=name,
            category=category,
            description=request.POST.get("description", ""),
            purchase_price=request.POST.get("purchase_price") or 0,
            selling_price=request.POST.get("selling_price") or 0,
            tax_rate=request.POST.get("tax_rate") or 19,
            minimum_stock=request.POST.get("minimum_stock") or 5,
        )

        messages.success(request, "تمت إضافة المنتج بنجاح.")
        return redirect("products:list")

    return render(
        request,
        "products/form.html",
        {"categories": categories},
    )


@login_required
@permission_required(
    "products.change_product",
    raise_exception=True,
)
@require_http_methods(["GET", "POST"])
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.filter(is_active=True)

    if request.method == "POST":
        code = (request.POST.get("code") or "").strip()
        name = (request.POST.get("name") or "").strip()
        category_id = request.POST.get("category")

        if not code or not name or not category_id:
            messages.error(
                request,
                "يرجى إدخال رمز المنتج واسمه واختيار الفئة."
            )
            return render(
                request,
                "products/form.html",
                {
                    "product": product,
                    "categories": categories,
                },
            )

        if Product.objects.filter(
            code=code
        ).exclude(pk=pk).exists():
            messages.error(
                request,
                "رمز المنتج مستخدم من طرف منتج آخر!"
            )
            return render(
                request,
                "products/form.html",
                {
                    "product": product,
                    "categories": categories,
                },
            )

        category = get_object_or_404(
            categories,
            pk=category_id,
        )

        product.code = code
        product.name = name
        product.category = category
        product.description = request.POST.get("description", "")
        product.purchase_price = request.POST.get("purchase_price") or 0
        product.selling_price = request.POST.get("selling_price") or 0
        product.tax_rate = request.POST.get("tax_rate") or 19
        product.minimum_stock = request.POST.get("minimum_stock") or 5

        product.save()

        messages.success(request, "تم تعديل المنتج بنجاح.")
        return redirect("products:list")

    return render(
        request,
        "products/form.html",
        {
            "product": product,
            "categories": categories,
        },
    )


@login_required
@permission_required(
    "products.delete_product",
    raise_exception=True,
)
@require_POST
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()

    messages.success(request, "تم حذف المنتج بنجاح.")
    return redirect("products:list")