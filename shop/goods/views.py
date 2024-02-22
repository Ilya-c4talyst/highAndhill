from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import Product, Brand, Banner, Size

import random


def index(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    return render(request, 'index.html', context=context)


def shoes(request):
    products = Product.objects.all()
    brands = Brand.objects.all()
    banners = Banner.objects.all()[:3]
    sizes = Size.objects.all()
    
    selected_brand = request.GET.get('brand')
    if selected_brand:
        products = products.filter(brand__id=selected_brand)

    selected_size = request.GET.get('sizes')
    if selected_size:
        products = products.filter(sizes__id=selected_size)

    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    
    try:
        goods = paginator.page(page)
    except PageNotAnInteger:
        goods = paginator.page(1)
    except EmptyPage:
        goods = paginator.page(paginator.num_pages)

    context = {
        'brands': brands,
        'goods': goods,
        'banners': banners,
        'sizes': sizes,
    }
    return render(request, 'catalog/shoes.html', context=context)


def shoescart(requeset, product_id):
    product = get_object_or_404(Product, id=product_id)
    all = Product.objects.all()
    ln_products = len(all)
    look_at = []
    for _ in range(3):
        look_at.append(all[random.randint(0, ln_products-1)])


    context = {
        'look_at': look_at,
        'product': product
    }

    return render(requeset, 'catalog/shoes_id.html', context=context)