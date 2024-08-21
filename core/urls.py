from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views





urlpatterns = [
    # path('login',login),
    #  path('register',register),
      path('auth/', include('djoser.urls')),
      path('auth/', include('djoser.urls.authtoken')),
      path('login/', views.login_view, name='login'),
      path('register/', views.register, name='register'),
     

]