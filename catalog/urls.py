from django.urls import path
from .views import HomeView, ContactView, FormContactsView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contact'),
    path('form_contacts/', FormContactsView.as_view(), name='form_contacts'),

    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]