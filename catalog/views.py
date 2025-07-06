from django.http import HttpResponse

from django.shortcuts import render


def home(request):
    return render(request,'home.html')

def contacts(request):
    return render(request, 'contacts.html')

def form_contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        return HttpResponse(f'Спасибо, {name}! Данные получены')

    return render(request, 'contacts.html')
