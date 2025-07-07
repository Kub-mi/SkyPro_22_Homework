from django.http import HttpResponse
from django.shortcuts import render
from catalog.models import Product


def home_view(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    print("🔍 Последние 5 продуктов:")
    for product in latest_products:
        print(f"{product.name} — {product.created_at}")

    return render(request, 'home.html', {'products': latest_products})

def contacts(request):
    return render(request, 'contacts.html')

def form_contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        return HttpResponse(f'Спасибо, {name}! Данные получены')

    return render(request, 'contacts.html')
