from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('order/', views.order),
    path('menu/', views.menu),
    path('menu/add-menu', views.addMenu, name='addMenu'),
    path('menu/delete-menu/<str:pk>', views.deleteMenu, name='deleteMenu'),
    path('menu/view-menu/<str:pk>', views.viewMenu, name='viewMenu'),
    path('menu/edit-menu/<str:pk>', views.editMenu, name='editMenu'),
    path('category/', views.category),
    path('category/add-category', views.addCategory, name='addCategory'),
    path('category/delete-category/<str:pk>', views.deleteCategory, name='deleteCategory'),
    path('category/view-category/<str:pk>', views.viewCategory, name='viewCategory'),
    path('category/edit-category/<str:pk>', views.editCategory, name='editCategory'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
