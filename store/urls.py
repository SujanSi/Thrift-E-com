
from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views
from django.contrib.auth import views as auth_views


from rest_framework.routers import SimpleRouter

routers=SimpleRouter()
routers.register('categories',CategoryViewset,basename='category')
routers.register('products',ProductViewset,basename='product')
routers.register('customers',CustomerViewset,basename='customer')
routers.register('carts',CartViewset,basename='cart')
routers.register('cart-items',CartItemViewset,basename='cart-items')
routers.register('orders',OrderViewset,basename='order')
routers.register('reviews',ReviewViewset,basename='review')

urlpatterns = [
    
    
    path('',views.homepage,name='home'),
   
    path('product/',views.productpage),
    
    path('products/<int:product_id>/', views.product_detail_view, name='product_detail'),
    
    path('cart/',views.cartpage),
    path('account/register/',views.register),
    
    
   path('account/',views.accountpage, name='account_page'),
   
    path('login/', views.login_view, name='login_view'),
    path('user_logout', views.user_logout, name = "user_logout"),
    
    path('add_to_cart/', views.add_to_cart, name="add_to_cart"),
    path('delete_cart/<int:item_id>/', views.delete_cart, name='delete_cart'), 

    path('checkout/', views.checkout, name='checkout'),

    path('khalti_payment/', views.khalti_payment, name='khalti_payment'),
    path('submit_khalti_payment/', views.submit_khalti_payment, name='submit_khalti_payment'),
        
    path('cart/', views.cartpage, name='cartpage'),
    
    path('orders/', views.order_list, name='order_list'),

    path('upload/', upload_product, name='upload_product'),

     path('my-orders/', my_product_orders, name='my_product_orders'),
   
]
