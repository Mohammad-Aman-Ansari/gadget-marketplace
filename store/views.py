from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Category, Gadget
from .forms import GadgetForm


def home(request):
    gadgets = Gadget.objects.filter(stock__gt=0).select_related('category', 'seller').order_by('-created_at')
    categories = Category.objects.all()

    # Read filter parameters from the URL (?q=...&category=...&condition=...)
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    condition = request.GET.get('condition', '').strip()

    if query:
        # Equivalent SQL: WHERE (title LIKE '%query%' OR brand LIKE '%query%' OR description LIKE '%query%')
        gadgets = gadgets.filter(
            Q(title__icontains=query) | Q(brand__icontains=query) | Q(description__icontains=query)
        )
    if category_slug:
        gadgets = gadgets.filter(category__slug=category_slug)
    if condition:
        gadgets = gadgets.filter(condition=condition)

    context = {
        'gadgets': gadgets,
        'categories': categories,
        'selected_category': category_slug,
        'selected_condition': condition,
        'search_query': query,
    }
    return render(request, 'store/home.html', context)


def sell_gadget(request):
    if request.method == 'POST':
        form = GadgetForm(request.POST, request.FILES)
        if form.is_valid():
            gadget = form.save(commit=False)
            # Assign logged-in user, or fallback to your first admin user until Phase 5 Auth
            gadget.seller = request.user if request.user.is_authenticated else User.objects.first()
            gadget.save()
            return redirect('home')
    else:
        form = GadgetForm()

    return render(request, 'store/sell.html', {'form': form})

