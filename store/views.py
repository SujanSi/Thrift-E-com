from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.decorators import action
from .pagination import CustomPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import *
from django_filters import rest_framework as filters
from rest_framework import filters as f
from .filters import ProductFilter
from django.db.models import Count, Prefetch
from django.urls import reverse
from django.shortcuts import render , redirect,  get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from django.contrib.auth import get_user_model,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import ProductForm



User=get_user_model() 


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Category.objects.prefetch_related(
            "products"
        ).annotate(
            total_product=Count('products')
        ).all()


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerialzer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend, f.SearchFilter,)
    filterset_class = ProductFilter
    search_fields = ('name',)


class CustomerViewset(viewsets.GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Customer.objects.get(user=user)

    def list(self, request, *args, **kwargs):
        customer = self.get_queryset()
        serializer = self.serializer_class(customer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        customer = self.get_queryset()
        context = {'request': request}
        serializer = self.serializer_class(data=request.data, instance=customer, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CartViewset(viewsets.ViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerailizer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        customer = Customer.objects.filter(user=self.request.user).first()
        cart, _ = Cart.objects.prefetch_related('items').get_or_create(customer=customer)
        serializer = CartSerailizer(cart)
        return Response(serializer.data)


class CartItemViewset(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        customer = Customer.objects.filter(user=self.request.user).first()
        cart, _ = Cart.objects.prefetch_related('items').get_or_create(customer=customer)
        return CartItem.objects.filter(
            cart=cart
        )


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('order_items').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Order.objects.prefetch_related('order_items').filter(
            customer__user=self.request.user
        )

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return CancelOrderSerializer
        return OrderSerializer


class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticated,
       
    )



@login_required
def upload_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.uploaded_by = request.user
            product.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'upload_product.html', {'form': form})



@login_required
def my_product_orders(request):
    # Filter OrderItems where the product was uploaded by the logged-in user
    orders = OrderItem.objects.filter(product__uploaded_by=request.user).select_related('order__customer__user')
    return render(request, 'my_product_orders.html', {'orders': orders})



def addproduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  
    else:
        form = ProductForm()
    categories = Category.objects.all()  # Fetch all categories from the database
    return render(request, 'store/add_product.html', {'form': form, 'categories': categories})

    
    
    
def homepage(request):
    return render(request,"index.html")


def productpage(request):

    products=Product.objects.all()
    context={
        'products':products
    }
    return render(request, "products.html",context=context)



def productdetailpage(request):
    
    return render(request, "productdetails.html")

def cartpage(request):
    return render(request, "cart.html")

def accountpage(request):
    # Method Post:
    if request.method=="POST":
        request_body=request.body
        
        print(request_body,"Request body")
        return redirect('home')
        # return render(request,"accounts.html",{'logged_in':True})
    
    
    # Method GET
    return render(request, "accounts.html")

def addprodcutpage(request):
    return render(request,"addproduct.html")


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different one.')
            return redirect('home') 
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered. Please use a different email address.')
            return redirect('home') 
        
        
        user = User.objects.create_user(username=username, email=email, password=password)
        
        if user:
            messages.success(request, 'User has been successfully created!')
            return redirect('home')  
        
    
    return render(request, 'register.html')
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # login(request)
                (request,user)
                # raise Exception(user)
                # Redirect to a success page or the homepage
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login_view')


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'productdetails.html', {'product': product})



@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size')
        
        product = get_object_or_404(Product, id=product_id)
        
        # Get the customer associated with the logged-in user
        customer = get_object_or_404(Customer, user=request.user)
        
        # Get or create a cart for the customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        
        # Check if the cart already has the item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        
        cart_item.save()
        
        return redirect('cartpage')

    return HttpResponse(status=405)



@login_required
@require_POST
def delete_cart(request, item_id):
    customer = get_object_or_404(Customer, user=request.user)
    cart = get_object_or_404(Cart, customer=customer)
    
    try:
        cart_item = CartItem.objects.get(cart=cart, product_id=item_id)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    
    return redirect(reverse('cartpage'))

@login_required
def cartpage(request):
    customer = get_object_or_404(Customer, user=request.user)
    cart = get_object_or_404(Cart, customer=customer)
    cart_items = CartItem.objects.filter(cart=cart)
    
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    
    shipping_charge = 100  # Fixed shipping charge
    total_price_with_shipping = subtotal + shipping_charge
    
    request.session['total_price_with_shipping'] = total_price_with_shipping
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_charge': shipping_charge,
        'total_price_with_shipping': total_price_with_shipping
    }
    return render(request, 'cart.html', context)


@login_required
@transaction.atomic
def checkout(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        payment_method = request.POST.get('payment_method')
        print("-----------")
        print(address)        
        print("-----------")
        # Get the customer instance
        customer = Customer.objects.get(user=request.user)

        # Create a new order
        order = Order.objects.create(
            customer=customer,
            shipping_address=address,
            payment_method=payment_method
        )

        # Get the cart items for the customer
        try:
            cart = Cart.objects.get(customer=customer)
            cart_items = CartItem.objects.filter(cart=cart)

            # Create order items and save them to the database
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            # Create order summary and save it to the database
            order_summary = OrderSummary.objects.create(
                order=order,
                total_price_with_shipping=request.session.get('total_price_with_shipping'),
                shipping_address=address,
                payment_method=payment_method
            )

            # Clear the cart
            cart_items.delete()


            

            context = {
                        'order': order,
                        'order_summary': order_summary,
                        'order_items': order.order_items.all(),
                        'mobile': mobile,
                        'show_popup': True
                    }
            
            if payment_method == 'khalti':
                    # Redirect to Khalti payment page
                return render(request, 'checkout.html', context)

            return render(request, 'cart.html', context)

            

        except Cart.DoesNotExist:
            return redirect('cartpage')

        
    return redirect('cartpage')











import requests
import json
import uuid
import hashlib
import base64
import hmac

def khalti_payment(request):
    # Generate a UUID for the transaction
    transaction_uuid = uuid.uuid4()

    # Retrieve grand total from session
    total_price_with_shipping = request.session.get('total_price_with_shipping')
    print("okie")
    print(total_price_with_shipping)
    # Convert grand total to paisa (assuming grand total is in rupees)
    amount = int(float(total_price_with_shipping) * 100)   # Convert rupees to paisa

    context = {
        'purchase_order_id': transaction_uuid,
        'amount': amount,
    }
    print("-----")
    print(amount)
    return render(request, 'khalti_payment.html', context)

def submit_khalti_payment(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        user = request.user
        purchase_order_id = request.POST.get('purchase_order_id')
        amount = request.POST.get('amount')
        return_url = request.POST.get('return_url')
        print("purchase_order_id",purchase_order_id)
        print("amount", amount)
        # Construct payload for Khalti payment initiation
        payload = {
            "return_url": return_url,  # Replace with your home URL
            "website_url": "http://localhost:8000",  # Replace with your website URL
            "amount": amount,  # Convert to string
            "purchase_order_id": purchase_order_id,  # Convert UUID to string
            "purchase_order_name": "Test Product",  # Replace with your product name
            "customer_info": {
                "name": user.username,  # Replace with customer's name
                "email": "test@khalti.com",  # Replace with customer's email
                "phone": "9800000001"  # Replace with customer's phone number 
            }
        }

        # Headers for Khalti API request
        headers = {
            "Authorization": "key live_secret_key_68791341fdd94846a146f0457ff7b455",
            'Content-Type': 'application/json',
        }

        # Khalti API endpoint for payment initiation
        url = "https://a.khalti.com/api/v2/epayment/initiate/"

        # Make a POST request to initiate Khalti payment
        # Make a POST request to initiate Khalti payment
        response = requests.post(url, headers=headers, json=payload)  # Fix here

        
        print(response.text)
        new_res = json.loads(response.text)
        return redirect(new_res['payment_url'])
    
    else:
        return HttpResponse("Invalid Request")
    

@login_required
def order_list(request):
    
    customer = Customer.objects.get(user=request.user)
    
    
    orders = Order.objects.filter(customer=customer).order_by('-created_at')
    
    context = {
        'orders': orders
    }
    return render(request, 'order_list.html', context)