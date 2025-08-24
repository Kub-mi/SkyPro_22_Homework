from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, View, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Category
from django.core.paginator import Paginator
from .services import get_category_product_ids, get_products_by_ids_preserving_order

from catalog.forms import ProductForm
from catalog.models import Product
from django.conf import settings



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
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f'Спасибо, {name}! Данные получены')


@method_decorator(
    cache_page(settings.PRODUCT_DETAIL_CACHE_TTL, key_prefix="product"),
    name="dispatch",
)

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_details.html'
    context_object_name = 'product'
    login_url = "login"
    redirect_field_name = "next"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = "login"
    redirect_field_name = "next"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = "login"
    redirect_field_name = "next"

    def test_func(self):
        return self.get_object().owner == self.request.user


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    login_url = "login"
    redirect_field_name = "next"
    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return obj.owner == user or user.has_perm("catalog.delete_product")


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublished_product'
    raise_exception = True

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.is_published:
            product.is_published = False
            product.save(update_fields=['is_published'])
            messages.success(request, "Публикация продукта отменена")
        else:
            messages.info(request, "Продукт уже не опубликован.")
        return redirect("catalog:product_details")


class CategoryProductsView(View):
    template_name = "catalog/category_products.html"
    per_page = 12  # как и раньше

    def get(self, request, pk: int):
        category = get_object_or_404(Category, pk=pk)

        # 1) из кеша — упорядоченный список ID
        all_ids = get_category_product_ids(category.id)

        # 2) пагинация по ID
        paginator = Paginator(all_ids, self.per_page)
        page_number = request.GET.get("page") or 1
        page_obj = paginator.get_page(page_number)

        # 3) достаем объекты одной пачкой, сохраняя порядок
        page_ids = list(page_obj.object_list)
        products = get_products_by_ids_preserving_order(page_ids)

        context = {
            "category": category,
            "products": products,  # список для рендера карточек
            "page_obj": page_obj,  # навигация пагинатора
        }
        return render(request, self.template_name, context)

