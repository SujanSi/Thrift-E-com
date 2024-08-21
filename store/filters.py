from django_filters import rest_framework as filters
from .models import Product

class ProductFilter(filters.FilterSet):
    class Meta:
        model=Product

        #product.objects.filter(price__gt=100price__lt)


        fields={
            'category':['exact'],
            'price':['gt','lt'],
            'quantity':['gt','lt']
        }
        