from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Menu, Category, Order, OrderItem
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# ORDER SECTION
def order(request):
    orders = Order.objects.all().prefetch_related('orderitem_set__menu')
    for order in orders:
        order.total_price = sum(order_item.total_price() for order_item in order.orderitem_set.all())
    return render(request, 'order.html', {'orders':orders})


# DASSHBOARD SECTION
def dashboard(request):
    return render(request, 'index.html')


# MENU SECTION
def menu(request):
    allMenu = Menu.objects.all()
    categories = Category.objects.all()
    return render(request, 'menu.html', {'allMenu':allMenu, 'categories':categories})

def addMenu(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        image = request.FILES.get('image')
        price = request.POST['price']
        rating = request.POST['rating']
        review = request.POST['review']
        category = request.POST['category'] 

        category_id = Category.objects.get(id=category)

        add_menu = Menu.objects.create(name=name, description=description, image=image, price=price, rating=rating, review=review, category=category_id)
        add_menu.save()
        return redirect("/menu")
    else:
        return render(request, 'menu.html')
    
def deleteMenu(request, pk):
    menu = Menu.objects.get(id=pk)
    menu.delete()
    return redirect("/menu")

# CATEGORY SECTION
def category(request):
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories':categories})

def addCategory(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        image = request.FILES.get('image')

        add_category = Category.objects.create(name=name, description=description, image=image)
        add_category.save()
        return redirect("/category")
    else:
        return render(request, 'category.html')
    
def deleteCategory(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    return redirect("/category")

# AUTH SECTION
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
