from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from catalog.models import Product


def home_view(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    print("🔍 Последние 5 продуктов:")
    for product in latest_products:
        print(f"{product.name} — {product.created_at}")

    return render(request, 'catalog/home.html', {'products': latest_products})

def contacts(request):
    return render(request, 'catalog/contacts.html')

def form_contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        return HttpResponse(f'Спасибо, {name}! Данные получены')

    return render(request, 'catalog/contacts.html')

def product_details(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    return render(request,'catalog/product_details.html', {'product': product})
