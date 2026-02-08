from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='home'),
    path('add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('home/', views.product_list, name='product_list'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
]
