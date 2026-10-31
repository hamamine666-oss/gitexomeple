from django.shortcuts import render, redirect, get_object_or_404
from .models import Purchase
from suppliers.models import Supplier


def purchase_list(request):

    purchases = Purchase.objects.select_related("supplier").all()

    search = request.GET.get("search", "")

    if search:
        purchases = purchases.filter(
            invoice_number__icontains=search
        ) | purchases.filter(
            supplier__name__icontains=search
        )

    context = {
        "purchases": purchases,
        "search": search,
    }

    return render(
        request,
        "purchases/list.html",
        context
    )


def purchase_create(request):

    suppliers = Supplier.objects.filter(is_active=True)

    if request.method == "POST":

        Purchase.objects.create(
            invoice_number=request.POST.get("invoice_number"),
            supplier_id=request.POST.get("supplier"),
            total_amount=request.POST.get("total_amount") or 0,
            paid_amount=request.POST.get("paid_amount") or 0,
            status=request.POST.get("status") or "pending",
            notes=request.POST.get("notes", ""),
        )

        return redirect("purchases:list")

    return render(
        request,
        "purchases/form.html",
        {
            "suppliers": suppliers,
        }
    )


def purchase_edit(request, pk):

    purchase = get_object_or_404(
        Purchase,
        pk=pk
    )

    suppliers = Supplier.objects.filter(is_active=True)

    if request.method == "POST":

        purchase.invoice_number = request.POST.get(
            "invoice_number"
        )

        purchase.supplier_id = request.POST.get(
            "supplier"
        )

        purchase.total_amount = (
            request.POST.get("total_amount") or 0
        )

        purchase.paid_amount = (
            request.POST.get("paid_amount") or 0
        )

        purchase.status = (
            request.POST.get("status") or "pending"
        )

        purchase.notes = request.POST.get(
            "notes",
            ""
        )

        purchase.save()

        return redirect("purchases:list")

    return render(
        request,
        "purchases/form.html",
        {
            "purchase": purchase,
            "suppliers": suppliers,
        }
    )


def purchase_delete(request, pk):

    purchase = get_object_or_404(
        Purchase,
        pk=pk
    )

    if request.method == "POST":
        purchase.delete()

    return redirect("purchases:list")