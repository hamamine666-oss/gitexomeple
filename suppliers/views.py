from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier


def supplier_list(request):

    suppliers = Supplier.objects.all()

    search = request.GET.get("search", "")

    if search:
        suppliers = suppliers.filter(
            name__icontains=search
        ) | suppliers.filter(
            company_name__icontains=search
        ) | suppliers.filter(
            phone__icontains=search
        ) | suppliers.filter(
            email__icontains=search
        )

    context = {
        "suppliers": suppliers,
        "search": search,
    }

    return render(
        request,
        "suppliers/list.html",
        context
    )


def supplier_create(request):

    if request.method == "POST":

        Supplier.objects.create(
            name=request.POST.get("name"),
            company_name=request.POST.get("company_name", ""),
            phone=request.POST.get("phone", ""),
            email=request.POST.get("email", ""),
            address=request.POST.get("address", ""),
            tax_number=request.POST.get("tax_number", ""),
            balance=request.POST.get("balance") or 0,
            notes=request.POST.get("notes", ""),
            is_active=request.POST.get("is_active") == "on",
        )

        return redirect("suppliers:list")

    return render(
        request,
        "suppliers/form.html"
    )


def supplier_edit(request, pk):

    supplier = get_object_or_404(
        Supplier,
        pk=pk
    )

    if request.method == "POST":

        supplier.name = request.POST.get("name")
        supplier.company_name = request.POST.get(
            "company_name",
            ""
        )
        supplier.phone = request.POST.get(
            "phone",
            ""
        )
        supplier.email = request.POST.get(
            "email",
            ""
        )
        supplier.address = request.POST.get(
            "address",
            ""
        )
        supplier.tax_number = request.POST.get(
            "tax_number",
            ""
        )
        supplier.balance = request.POST.get(
            "balance"
        ) or 0
        supplier.notes = request.POST.get(
            "notes",
            ""
        )
        supplier.is_active = (
            request.POST.get("is_active") == "on"
        )

        supplier.save()

        return redirect("suppliers:list")

    return render(
        request,
        "suppliers/form.html",
        {
            "supplier": supplier,
        }
    )


def supplier_delete(request, pk):

    supplier = get_object_or_404(
        Supplier,
        pk=pk
    )

    if request.method == "POST":
        supplier.delete()

    return redirect("suppliers:list")
