from django.urls import path
from .views import HomeView, ContactView, FormContactsView, ProductDetailView, AddProductView


app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contact'),
    path('form_contacts/', FormContactsView.as_view(), name='form_contacts'),
    path('product_details/<int:id>/', ProductDetailView.as_view(), name='product_details'),
    path('add_product/', AddProductView.as_view(), name='add_product'),
]