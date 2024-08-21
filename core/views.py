from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import *
from django.core.mail import send_mail
from django.contrib.auth import  authenticate
from django.contrib.auth import  login as L
from django.shortcuts import render , redirect
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(username=email, password=password)
    print(user)
    # if user:
    #     token, _ = Token.objects.get_or_create(user=user)

    return Response({
            'user': user.get_username(),
            # 'token': token.key
        })
    
    return Response("invalid")

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    password = serializer.validated_data.get('password')
    user = User.objects.create_user(email=email, password=password)

    if user:
        send_mail(
            "Welcome to Ecommerce",
            "Hello " + user.email + ". Welcome to Ecommerce",  # Added space after "Hello"
            "hello@gmail.com",
            [user.email]
        )
        return Response('User has been created successfully')
    
    return Response("Something went wrong")

# Example request data
"""
{ 
    "email": "hello@gmail.com",
    "password": "1234",
    "confirm_password": "1234"
}
"""
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # login(request)
                L(request,user)
                # raise Exception(user)
                # Redirect to a success page or the homepage
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 # login(request)
#                 L(request,user)
#                 # raise Exception(user)
#                 # Redirect to a success page or the homepage
#                 return redirect('home')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})

def register(request):
    user = None
    if request.method == 'POST':
        # print(request.POST)
        # form = UserCreationForm(request.POST)
        username = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_pass = request.POST.get('password2')
        if password != confirm_pass:
            return render(request, 'accounts.html', {'error': 'Passwords do not match'})
        
        UserModel = get_user_model()
        created_user = UserModel.objects.create_user(
            username=username,
            password=password
        )
        return render(request, 'accounts.html', {'created_user': created_user})
        # print(form.errors)
        # if form.is_valid():
        #     form.save()
        #     # return redirect('login')
        #     return render(request, 'accounts.html', {})
    else:
        form = UserCreationForm()
    return render(request, 'accounts.html', {'form': form, 'user': user})