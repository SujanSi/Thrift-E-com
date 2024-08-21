from rest_framework import serializers
from .models import *
from django.db import transaction 

class CategorySerializer(serializers.ModelSerializer):
    total_product=serializers.IntegerField()
    class Meta:
        model=Category
        fields=('id','name','total_product')
        
    # def get_total_product(self,category:Category):
    #     return category.products.count()
     
class SimpleCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Category
        fields=('id','name',)   
        
class ProductSerialzer(serializers.ModelSerializer):
    price_with_tax=serializers.SerializerMethodField()
    category_id=serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
        ,source='category'
    )
    category=SimpleCategorySerializer(read_only=True)
    class Meta:
        model=Product
        fields=(
            "name",
            "quantity",
            "price",
            "discounted_price",
            "price_with_tax",
            "category_id",
            "category"
        )
    
    def get_price_with_tax(self,product:Product):
        return (product.discounted_price * 0.13 )+product.discounted_price
        
    
class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    first_name=serializers.CharField(required=True)
    middle_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    address=serializers.CharField(required=True)
    gender=serializers.ChoiceField(required=True,choices=Customer.GENDER_CHOICES)
    class Meta:
        model = Customer
        fields = "__all__"
        
        



class CartItemSerializer(serializers.ModelSerializer):
    product_id=serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
    source="product"
    )
    product=ProductSerialzer(read_only=True)
    class Meta:
        model = CartItem
        fields=[
            'id',
            'product_id',
            'quantity',
            'product',
        ]
        
    def create(self, validated_data):
        request=self.context['request']
        
        cart=Cart.objects.get(customer__user=request.user)
        validated_data.update({
            'cart':cart
        })
        return super().create(validated_data)
        


class CartSerailizer(serializers.ModelSerializer):
    
    customer=serializers.StringRelatedField(
    )
    customer_id=serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source='customer'
    )
    items=CartItemSerializer(many=True)
    class Meta:
        model=Cart
        fields="__all__"
        





class CancelOrderSerializer(serializers.ModelSerializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    shipping_address=serializers.CharField(read_only=True)
    class Meta:
        model=Order
        fields=[
            'id',
            'shipping_address',
            'user'
        ]
        
    def update(self, instance, validated_data):
        instance.status=Order.CANCEL_CHOICES
        instance.save()
        return super().update(instance, validated_data)

  
    
    
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields="__all__"
    


class OrderSerializer(serializers.ModelSerializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    items=serializers.SerializerMethodField()
    class Meta:
        model=Order
        fields="__all__"
        
    
    def get_items(self,order:Order):
        return OrderItemSerializer(order.order_items.all(),many=True).data

    @transaction.atomic()
    def create(self, validated_data):

        customer=Customer.objects.get(user=validated_data.get('user'))
        cart=Cart.objects.get(customer=customer)
        cart_items=CartItem.objects.filter(cart=cart)
        order=Order.objects.create(
            customer=customer,
            shipping_address=validated_data.get('shipping_address'),
            status=Order.CONFIRM_CHOICES
        )
        order_item_objects=[
           OrderItem(
               product=item.product,
                price=item.product.price,
                quantity=item.quantity,
               order=order,
           )
        for item in cart_items
        ]
        
        OrderItem.objects.bulk_create(order_item_objects)
        cart.delete()
        return order
    
    
    
        

class ReviewSerializer(serializers.ModelSerializer):
    customer=serializers.StringRelatedField(required=False)
    class Meta:
        model=Review
        fields=[
            "id",
            "product",
            "star",
            "customer"
        ]
        
        
    def create(self, validated_data):
        request=self.context['request']
        customer=Customer.objects.get(user=request.user)
        review=Review.objects.create(
            customer=customer,
            **validated_data         
            )
        return review
    
    
    def update(self, instance, validated_data):
        instance.product=validated_data['product']
        instance.star=validated_data['star']
        instance.save()
        return instance