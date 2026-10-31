from django.shortcuts import render
from django.utils import timezone

from sales.models import Sale


def dashboard(request):
    today = timezone.localdate()

    recent_sales = Sale.objects.all().order_by('-id')[:10]

    context = {
        'recent_sales': recent_sales,
        # أضف هنا بقية إحصائيات لوحة التحكم
    }

    return render(request, 'dashboard.html', context)