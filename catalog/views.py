from unicodedata import category

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from catalog.models import Product, Category
from django.views.generic import ListView, DetailView, TemplateView, View, CreateView


# def home_view(request):
#     products = Product.objects.all()
#     paginator = Paginator(products, 6)
#
#     page_num = request.GET.get('page')
#     page_obj = paginator.get_page(page_num)
#     return render(request, 'catalog/home.html', {'page_obj': page_obj})

class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'page_obj'
    paginate_by = 6


# def contacts(request):
#     return render(request, 'catalog/contacts.html')


class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'


# def form_contacts(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#
#         return HttpResponse(f'Спасибо, {name}! Данные получены')
#
#     return render(request, 'catalog/contacts.html')


class FormContactsView(View):
    def get(self, request):
        return render(request, 'catalog/contacts.html')

    def post(self, request):
        name = request.Post.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f'Спасибо, {name}! Данные получены')

# def product_details(request, id):
#     product = get_object_or_404(Product, id=id)
#     return render(request,'catalog/product_details.html', {'product': product})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_details.html'
    context_object_name = 'product'
    pk_url_kwarg = 'id'


# def add_product(request):
#     if request.method == "POST":
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         image = request.FILES.get('image')
#         category_id = request.POST.get('category')
#         price = request.POST.get('price')
#
#         category = Category.objects.get(pk=category_id)
#
#         Product.objects.create(
#             name=name,
#             description=description,
#             image=image,
#             category=category,
#             price=price
#         )
#
#         return redirect('/catalog/')
#     categories = Category.objects.all()
#     return render(request,'catalog/add_product.html', {'categories': categories})


class AddProductView(CreateView):
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price']
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context