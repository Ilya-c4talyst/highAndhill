from django.shortcuts import render
from .models import Product, Brand, Banner

import random


def index(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    return render(request, 'index.html', context=context)


def catalog(request):
    products = Product.objects.all()
    brands = Brand.objects.all()
    banners = Banner.objects.all()[:3]
    selected_brand = request.GET.get('brand')
    if selected_brand:
        products = products.filter(brand__id=selected_brand)
    context = {
        'brands': brands,
        'goods': products,
        'banners': banners,
    }
    return render(request, 'catalog/list_products.html', context=context)
