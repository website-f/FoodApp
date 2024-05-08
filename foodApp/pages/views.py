from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Menu, Category, Order, OrderItem
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from datetime import datetime, timedelta
from django.db.models import Count

# ORDER SECTION
def order(request):
    orders = Order.objects.all().prefetch_related('orderitem_set__menu')
    for order in orders:
        order.total_price = sum(order_item.total_price() for order_item in order.orderitem_set.all())
    return render(request, 'order.html', {'orders':orders})


# DASHBOARD SECTION
def dashboard(request):

    #count total
    orderCount = Order.objects.all().count()
    menuCount = Menu.objects.all().count()
    allCategory = Category.objects.all().count()

    #recent sales
    allOrder = Order.objects.all().prefetch_related('orderitem_set__menu')
    for order in allOrder:
        order.total_price = sum(order_item.total_price() for order_item in order.orderitem_set.all())

    #top selling
    top_selling_menu = Menu.objects.annotate(num_orders=Count('order')).order_by('-num_orders')
    for menu in top_selling_menu:
        menu.revenue = menu.order_set.count() * menu.price

    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)

    # Fetching the data for each day
    data = []
    for i in range(7):
        date = start_date + timedelta(days=i)
        orders = Order.objects.filter(created_at__date=date).count()
        menus = Menu.objects.filter(created_at__date=date).count()
        categories = Category.objects.filter(created_at__date=date).count()
        data.append({'date': date.strftime("%Y-%m-%d"), 'orders': orders, 'menus': menus, 'categories': categories})
    
    return render(request, 'index.html', {'orderCount':orderCount, 'menuCount':menuCount, 'allCategory':allCategory, 'data':data, 'allOrder':allOrder, 'top_selling_menu':top_selling_menu})


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

def viewMenu(request, pk):
    menu = Menu.objects.get(id=pk)
    categories = Category.objects.all()
    return render(request, 'viewMenu.html', {'menu':menu, 'categories':categories})

def editMenu(request, pk):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        image = request.FILES.get('image')
        price = request.POST['price']
        rating = request.POST['rating']
        review = request.POST['review']
        category = request.POST['category'] 

        menu = Menu.objects.get(id=pk) 
        if image:
            menu.name = name
            menu.description = description 
            menu.image = image
            menu.price = price
            menu.rating = rating
            menu.review = review
            category_id = Category.objects.get(id=category)
            menu.category = category_id
            menu.save()
            return redirect('viewMenu', pk=pk)
        else:
            menu.name = name
            menu.description = description
            menu.price = price
            menu.rating = rating
            menu.review = review
            category_id = Category.objects.get(id=category)
            menu.category = category_id
            menu.save()
            return redirect('viewMenu', pk=pk)
    else:
         menu = Menu.objects.get(id=pk) 
         return render(request, 'viewMenu.html', {'menu':menu})
    

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

def viewCategory(request, pk):
    category = Category.objects.get(id=pk)
    return render(request, 'viewCategory.html', {'category':category})

def editCategory(request, pk):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        image = request.FILES.get('image')

        category = Category.objects.get(id=pk) 
        if image:
            category.name = name
            category.description = description 
            category.image = image
            category.save()
            return redirect('viewCategory', pk=pk)
        else:
            category.name = name
            category.description = description
            category.save()
            return redirect('viewCategory', pk=pk)
    else:
         category = Category.objects.get(id=pk) 
         return render(request, 'viewCategory.html', {'category':category})
    

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
