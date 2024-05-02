from django.shortcuts import render
from django.http import HttpResponse

def order(request):
    return render(request, 'order.html')

def dashboard(request):
    return render(request, 'index.html')

def menu(request):
    return render(request, 'menu.html')