from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns  = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contact'),
    path('form_contacts/', views.form_contacts, name='form_contacts'),
]