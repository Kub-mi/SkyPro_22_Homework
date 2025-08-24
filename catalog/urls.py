from django.urls import path
from .views import HomeView, ContactView, FormContactsView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, ProductUnpublishView, CategoryProductsView
from django.conf import settings
from django.conf.urls.static import static


app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contact'),
    path('form_contacts/', FormContactsView.as_view(), name='form_contacts'),

    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/<int:pk>/unpublish/', ProductUnpublishView.as_view(), name='product_unpublish'),
    path("categories/<int:pk>/", CategoryProductsView.as_view(), name="category_products"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)