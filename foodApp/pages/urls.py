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

    #API
    path('api/categories', views.get_all_categories),
    path('api/menus', views.get_all_menus),
    path('api/order', views.create_order),
    path('api/top-seller', views.top_sellers),
    path('menu/<int:menu_id>/submit-review/', views.submit_review),
    path('menu/<int:menu_id>/reviews/', views.get_reviews_for_menu, name='get_reviews_for_menu'),
    path('api/recommended/', views.get_recommended_menus),

    #auth
    path('api/login', views.api_login),
    path('api/logout', views.api_logout),
    path('api/current-user', views.api_current_user),
    path('api/login-stat', views.api_login_stat),
    path('api/register', views.api_register),

]
