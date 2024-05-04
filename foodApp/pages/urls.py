from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('order/', views.order),
    path('menu/', views.menu),
    path('menu/add-menu', views.addMenu, name='addMenu'),
    path('menu/delete-menu/<str:pk>', views.deleteMenu, name='deleteMenu'),
    path('category/', views.category),
    path('category/add-category', views.addCategory, name='addCategory'),
    path('category/delete-category/<str:pk>', views.deleteCategory, name='deleteCategory'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
