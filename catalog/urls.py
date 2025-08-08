from django.urls import path
from . import views
from .views import HomeView, ContactView, FormContactsView, ProductDetailView, AddProductView

# urlpatterns  = [
#     path('', views.home_view, name='home'),
#     path('contacts/', views.contacts, name='contact'),
#     path('form_contacts/', views.form_contacts, name='form_contacts'),
#     path('product_details/<int:id>/', views.product_details, name='product_details'),
#     path('add_product/', views.add_product, name='add_product'),
# ]

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contact'),
    path('form_contacts/', FormContactsView.as_view(), name='form_contacts'),
    path('product_details/<int:id>/', ProductDetailView.as_view(), name='product_details'),
    path('add_product/', AddProductView.as_view(), name='add_product'),
]