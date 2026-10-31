
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Sale
from .forms import SaleForm, SaleItemFormSet


@login_required
@permission_required("sales.view_sale", raise_exception=True)
def sale_list(request):
    sales = (
        Sale.objects
        .select_related("customer")
        .prefetch_related("items__product")
        .order_by("-sale_date", "-pk")
    )

    search = request.GET.get("search", "").strip()

    if search:
        sales = sales.filter(
            invoice_number__icontains=search
        )

    # تقسيم الفواتير إلى صفحات، 5 فواتير لكل صفحة
    paginator = Paginator(sales, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "sales/list.html", {
        "sales": page_obj.object_list,
        "page_obj": page_obj,
        "search": search,
    })


@login_required
@permission_required("sales.add_sale", raise_exception=True)
def sale_create(request):
    is_ajax = (
        request.headers.get("X-Requested-With")
        == "XMLHttpRequest"
    )

    if request.method == "POST":
        form = SaleForm(request.POST)

        item_formset = SaleItemFormSet(
            request.POST,
            prefix="items",
        )

        if form.is_valid() and item_formset.is_valid():
            with transaction.atomic():
                sale = form.save(commit=False)
                items = item_formset.save(commit=False)

                total = Decimal("0.00")

                for item in items:
                    item.total_price = (
                        item.quantity * item.unit_price
                    )
                    total += item.total_price

                sale.total_amount = total
                sale.save()

                for item in items:
                    item.sale = sale
                    item.save()

                item_formset.save_m2m()

            if is_ajax:
                return JsonResponse({
                    "success": True,
                    "message": "تم حفظ الفاتورة وجميع المنتجات بنجاح.",
                })

            return redirect("sales:list")

    else:
        form = SaleForm()
        item_formset = SaleItemFormSet(prefix="items")

    return render(request, "sales/form_modal.html", {
        "form": form,
        "item_formset": item_formset,
        "sale": None,
        "is_modal": is_ajax,
    })


@login_required
@permission_required("sales.change_sale", raise_exception=True)
def sale_edit(request, pk):
    is_ajax = (
        request.headers.get("X-Requested-With")
        == "XMLHttpRequest"
    )

    sale = get_object_or_404(
        Sale.objects.prefetch_related("items"),
        pk=pk,
    )

    if request.method == "POST":
        form = SaleForm(
            request.POST,
            instance=sale,
        )

        item_formset = SaleItemFormSet(
            request.POST,
            instance=sale,
            prefix="items",
        )

        if form.is_valid() and item_formset.is_valid():
            with transaction.atomic():
                sale = form.save(commit=False)
                items = item_formset.save(commit=False)

                for deleted_item in item_formset.deleted_objects:
                    deleted_item.delete()

                total = Decimal("0.00")

                for item in items:
                    item.total_price = (
                        item.quantity * item.unit_price
                    )
                    total += item.total_price

                sale.total_amount = total
                sale.save()

                for item in items:
                    item.sale = sale
                    item.save()

                item_formset.save_m2m()

            if is_ajax:
                return JsonResponse({
                    "success": True,
                    "message": "تم تعديل الفاتورة بنجاح.",
                })

            return redirect("sales:list")

    else:
        form = SaleForm(instance=sale)

        item_formset = SaleItemFormSet(
            instance=sale,
            prefix="items",
        )

    return render(request, "sales/form_modal.html", {
        "form": form,
        "item_formset": item_formset,
        "sale": sale,
        "is_modal": is_ajax,
    })


@login_required
@permission_required("sales.delete_sale", raise_exception=True)
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)

    if request.method == "POST":
        sale.delete()

    return redirect("sales:list")


@login_required
@permission_required("sales.view_sale", raise_exception=True)
def sale_detail(request, pk):
    sale = get_object_or_404(
        Sale.objects
        .select_related("customer")
        .prefetch_related("items__product"),
        pk=pk,
    )

    return render(
        request,
        "sales/detail_modal.html",
        {"sale": sale},
    )

