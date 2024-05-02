from django.contrib import admin
from .models import Category, Menu, Order, OrderItem, Customer

# Register your models here.

# Category Model
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'image']

admin.site.register(Category, CategoryAdmin)


# Menu Model
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'image', 'price', 'rating', 'review', 'category']

admin.site.register(Menu, MenuAdmin)

# Order Model
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'name', 'phone_number', 'email', 'status', 'created_at']

admin.site.register(Order, OrderAdmin)

# Order Item Model
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'menu', 'quantity']

admin.site.register(OrderItem, OrderItemAdmin)

# Customer Model
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'password']

admin.site.register(Customer, CustomerAdmin)
