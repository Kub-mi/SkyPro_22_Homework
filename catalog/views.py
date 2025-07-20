from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from catalog.models import Product


def home_view(request):
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products})


def contacts(request):
    return render(request, 'catalog/contacts.html')


def form_contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        return HttpResponse(f'Спасибо, {name}! Данные получены')

    return render(request, 'catalog/contacts.html')


def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request,'catalog/product_details.html', {'product': product})
