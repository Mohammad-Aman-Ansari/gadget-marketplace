from django.shortcuts import render
from .models import Category, Gadget


def home(request):
    # Equivalent SQL: SELECT * FROM store_gadget WHERE stock > 0 ORDER BY created_at DESC;
    gadgets = Gadget.objects.filter(stock__gt=0).select_related('category', 'seller').order_by('-created_at')
    categories = Category.objects.all()

    context = {
        'gadgets': gadgets,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)