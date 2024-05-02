from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard),
    path('order/', views.order),
    path('menu/', views.menu),
]
