from unicodedata import category

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from catalog.models import Product, Category


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


def add_product(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        category_id = request.POST.get('category')
        price = request.POST.get('price')

        category = Category.objects.get(pk=category_id)

        Product.objects.create(
            name=name,
            description=description,
            image=image,
            category=category,
            price=price
        )

        return redirect('home')
    categories = Category.objects.all()
    return render(request,'catalog/add_product/html', {'categories': categories})