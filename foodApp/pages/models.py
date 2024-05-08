from django.db import models
from datetime import datetime

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='category_images')
    created_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="menu_images")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True)
    review = models.TextField(default=None, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.name
    
class Order(models.Model):
    order_id = models.CharField(max_length=100) 
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=100, default=None, null=True)
    status_choice = [
        ('pending', 'Pending'),
        ('complete', 'Complete'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=status_choice)
    menu = models.ManyToManyField(Menu, through='OrderItem')
    created_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
            return f"{self.name}'s Orders"
    
class OrderItem(models.Model):
     order = models.ForeignKey(Order, on_delete=models.CASCADE)
     menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
     quantity = models.PositiveIntegerField()

     def total_price(self):
        return self.quantity * self.menu.price

     def __str__(self):
            return f"{self.quantity} x {self.menu.name} in Order {self.order.order_id}"

class Customer(models.Model):
     name = models.CharField(max_length=200)
     email = models.CharField(max_length=100)
     phone_number = models.CharField(max_length=20)
     password = models.CharField(max_length=100)

     def __str__(self):
        return self.name
