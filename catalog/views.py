from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from catalog.models import Product, Category
from django.views.generic import ListView, DetailView, TemplateView, View, CreateView


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'page_obj'
    paginate_by = 6


class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'


class FormContactsView(View):
    def get(self, request):
        return render(request, 'catalog/contacts.html')

    def post(self, request):
        name = request.Post.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f'Спасибо, {name}! Данные получены')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_details.html'
    context_object_name = 'product'
    pk_url_kwarg = 'id'


class AddProductView(CreateView):
    model = Product
    fields = ['name', 'description', 'image', 'category', 'price']
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context