from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('order/', views.order),
    path('menu/', views.menu),
    path('category/', views.category),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]
