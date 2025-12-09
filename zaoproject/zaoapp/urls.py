from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('base/', views.base, name='base'),  # Default URL/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.cart, name='cart'),
    path('dashboard/products/', views.product_admin_list, name='product_admin_list'),
    path('dashboard/products/add/', views.product_create, name='product_create'),
    path('dashboard/products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('dashboard/products/<int:pk>/delete/', views.product_delete, name='product_delete'),
]
