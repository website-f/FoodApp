from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Menu, Category, Order
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def order(request):
    orders = Order.objects.all()
    return render(request, 'order.html', {'orders':orders})

def dashboard(request):
    return render(request, 'index.html')

def menu(request):
    allMenu = Menu.objects.all()
    return render(request, 'menu.html', {'allMenu':allMenu})

def category(request):
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories':categories})

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            return redirect("dashboard")
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth_logout(request)
    return redirect("login")