import json
from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Category, Gadget, Order, OrderItem
from .forms import GadgetForm


def home(request):
    gadgets = Gadget.objects.filter(stock__gt=0).select_related('category', 'seller').order_by('-created_at')
    categories = Category.objects.all()

    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    condition = request.GET.get('condition', '').strip()

    if query:
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


@login_required(login_url='login')
def sell_gadget(request):
    if request.method == 'POST':
        form = GadgetForm(request.POST, request.FILES)
        if form.is_valid():
            gadget = form.save(commit=False)
            gadget.seller = request.user
            gadget.save()
            return redirect('home')
    else:
        form = GadgetForm()
    return render(request, 'store/sell.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'store/auth.html', {'form': form, 'title': 'Create an Account'})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/auth.html', {'form': form, 'title': 'Login to GadgetHub'})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def checkout(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    data = json.loads(request.body)
    items = data.get('items', [])
    address = data.get('address', '').strip()

    if not items or not address:
        return JsonResponse({'error': 'Cart items and delivery address are required.'}, status=400)

    order = Order.objects.create(buyer=request.user, shipping_address=address, total_amount=Decimal('0.00'))
    total = Decimal('0.00')

    for item in items:
        gadget = Gadget.objects.filter(id=item['id'], stock__gt=0).first()
        if gadget:
            qty = min(int(item['qty']), gadget.stock)
            OrderItem.objects.create(order=order, gadget=gadget, quantity=qty, price=gadget.price)
            gadget.stock -= qty
            gadget.save()
            total += gadget.price * qty

    order.total_amount = total
    order.save()
    return JsonResponse({'success': True, 'redirect_url': '/my-orders/'})


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(buyer=request.user).prefetch_related('items__gadget').order_by('-created_at')
    return render(request, 'store/orders.html', {'orders': orders})