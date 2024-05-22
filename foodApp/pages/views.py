from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Menu, Category, Order, OrderItem, Customer, Review
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from datetime import datetime, timedelta
from django.db.models import Count
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import models  # Add this line
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.utils import IntegrityError

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
        category = request.POST['category'] 

        category_id = Category.objects.get(id=category)

        add_menu = Menu.objects.create(name=name, description=description, image=image, price=price, category=category_id)
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


#API
def get_all_categories(request):
    categories = Category.objects.all().values('id', 'name', 'description', 'image')
    response = JsonResponse(list(categories), safe=False)
    response['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    return response

def get_all_menus(request):
    menus = Menu.objects.all().values('id', 'name', 'description', 'image', 'price', 'category__id', 'category__name')
    response = JsonResponse(list(menus), safe=False)
    response['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    return response

def top_sellers(request):
    top_sellers = OrderItem.objects.values('menu__name', 'menu__image').annotate(count=Count('id')).order_by('-count')[:5] #desc
    response = JsonResponse(list(top_sellers), safe=False)
    response['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
    return response

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try: 
            data = json.loads(request.body) #data yg kita submit

            order = Order.objects.create(
                order_id = data['order_id'],
                name = data['name'],
                phone_number = data['phone_number'],
                status = data.get('status', 'pending'),
            )

            for item in data['menu']:
                menu_item = Menu.objects.get(id=item['id'])
                OrderItem.objects.create(
                    order = order,
                    menu = menu_item,
                    quantity = item['quantity']
                )

            return JsonResponse({'message' : 'Order created successfully', 'order_id' : order.order_id}, status=201)
        
        except Exception as e:
            return JsonResponse({'error' : str(e)}, status=400)
    
    return JsonResponse({'error' : 'Invalid request method'}, status=405)

#API AUTH
@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            username = data.get('username')
            password = data.get('password')

            print(f"Login attempt with username: {username}, password: {password}")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                customer = Customer.objects.get(user=user)
                user_details = {
                    'name': user.username,  # Or user.first_name + " " + user.last_name
                    'phoneNumber': customer.phone_number,
                }
                print(user_details)
                return JsonResponse({'success': True, 'message': 'Login successful', **user_details})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
        except KeyError:
            return JsonResponse({'success': False, 'message': 'Invalid data'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

def api_logout(request):
    logout(request)
    return JsonResponse({'success': True, 'message': 'Logout successful'})

def api_current_user(request):
    if request.user.is_authenticated:
        current_user = {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            # Add more user information as needed
        }
        return JsonResponse(current_user)
    else:
        return JsonResponse({'message': 'User is not authenticated'}, status=401)

@login_required
def api_login_stat(request):
    user = request.user
    try:
        customer = user.customer  # Access the related Customer instance
        phone_number = customer.phone_number
    except Customer.DoesNotExist:
        phone_number = None

    return JsonResponse({
        'is_logged_in': True,
        'username': user.username,
        'email': user.email,
        'phoneNumber': phone_number
    })

@csrf_exempt
def api_register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Request Payload Data:", data)
            name = data['name']
            email = data['email']
            password = data['password']
            phone_number = data.get('phoneNumber', '')  # Get phone number from request data

            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already registered'}, status=400)
            
            # Create user
            user = User.objects.create(
                username=name,
                email=email,
                first_name=name,
                password=make_password(password)
            )

            # Create customer with user association
            customer = Customer.objects.create(
                user=user,
                phone_number=phone_number  # Insert phone number into Customer table
            )

            return JsonResponse({'success': 'User registered successfully'}, status=201)
        except KeyError:
            return JsonResponse({'error': 'Invalid data'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def submit_review(request, menu_id):
    if request.method == 'POST':
        # Get data from request (rating and review)
        data = json.loads(request.body)
        rating = data.get('rating')
        review_text = data.get('review_text')

        print(rating, review_text)

        # Validate data (you can add more validation if needed)
        if not rating or not review_text:
            return JsonResponse({'error': 'Rating or review text is missing'}, status=400)

        try:
            # Create the review object
            review = Review.objects.create(
                menu_id=menu_id,
                customer=request.user.customer,  # Assuming user is authenticated and has a customer profile
                rating=rating,
                review_text=review_text
            )

            # Return a JSON response indicating success
            return JsonResponse({'message': 'Review submitted successfully'})
        except IntegrityError:
            return JsonResponse({'error': 'Failed to submit review'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_reviews_for_menu(request, menu_id):
    try:
        reviews = Review.objects.filter(menu_id=menu_id).values('id', 'customer__user__username', 'rating', 'review_text')
        return JsonResponse(list(reviews), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def get_recommended_menus(request):
    # Get the current user
    current_user = request.user.customer

    # Get menus reviewed by the current user
    reviewed_menu_ids = Review.objects.filter(customer=current_user).values_list('menu_id', flat=True)

    reviewed_categories = Menu.objects.filter(id__in=reviewed_menu_ids).values_list('category', flat=True)

    # Exclude reviewed menus and get recommended menus
    recommended_menus = Menu.objects.filter(category__in=reviewed_categories).distinct()

    # Serialize the recommended menus data
    recommended_menus_data = list(recommended_menus.values())

    return JsonResponse(recommended_menus_data, safe=False)