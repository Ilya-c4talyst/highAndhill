import random
import secrets
import string
import json
import time

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


from .models import Product, Brand, Banner, Size, Type, Order, Cloth, ClothSize


def index(request):
    products = Product.objects.all()
    ln = len(products)
    products = products[ln-4:]
    liked = Product.objects.filter(most_liked=True)
    type = get_object_or_404(Type, name="main")
    banners = type.banners.all()
    ln = len(banners)
    banner = banners[random.randint(0, ln-1)]
    context = {
        'liked': liked,
        "goods": products,
        'banner': banner
    }
    return render(request, 'index.html', context=context)


def popular(request):
    products = Product.objects.filter(most_liked=True)
    context = {
        "goods": products,
    }
    return render(request, 'liked/liked.html', context=context)


def newest(request):
    products = Product.objects.all().order_by('-id')
    context = {
        "goods": products,
    }
    return render(request, 'liked/newest.html', context=context)


def sale(request):
    products = Product.objects.filter(on_sale=True)
    context = {
        "goods": products,
    }
    return render(request, 'liked/sale.html', context=context)


def shoes(request):

    type = get_object_or_404(Type, name="shoes")
    banners = type.banners.all()
    ln = len(banners)
    info = []
    for _ in range(3):
        info.append(banners[random.randint(0, ln-1)])
    
    products = Product.objects.filter(type__name="shoes")
    brands = Brand.objects.all()
    sizes = Size.objects.all()

    selected_brands = request.GET.getlist('brands')
    if selected_brands:
        products = products.filter(brand__id__in=selected_brands)

    # Фильтр по размерам
    selected_sizes = request.GET.getlist('sizes')
    if selected_sizes:
        products = products.filter(sizes__id__in=selected_sizes)

    search_query = request.GET.get('search_query')
    if search_query:
        products = products.filter(name__icontains=search_query)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    flag = True
    if len(products) <= 0:
        flag = False

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
        'banners': info,
        'sizes': sizes,
        'flag': flag
    }
    return render(request, 'catalog/shoes.html', context=context)


def clothes(request):

    type = get_object_or_404(Type, name="clothes")
    banners = type.banners.all()
    ln = len(banners)
    info = []
    for _ in range(3):
        info.append(banners[random.randint(0, ln-1)])
    
    products = Cloth.objects.filter(type__name="clothes")
    brands = Brand.objects.all()
    sizes = ClothSize.objects.all()

    selected_brands = request.GET.getlist('brands')
    if selected_brands:
        products = products.filter(brand__id__in=selected_brands)

    # Фильтр по размерам
    selected_sizes = request.GET.getlist('sizes')
    if selected_sizes:
        products = products.filter(sizes__id__in=selected_sizes)

    search_query = request.GET.get('search_query')
    if search_query:
        products = products.filter(name__icontains=search_query)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    flag = True
    if len(products) <= 0:
        flag = False

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
        'banners': info,
        'sizes': sizes,
        'flag': flag
    }
    return render(request, 'catalog/clothes.html', context=context)


def shoescart(request, product_id):
    if request.method == 'POST':
        size = request.POST.get('size') 
        product = get_object_or_404(Product, id=product_id)
        
        cart = request.session.get('cart', {})
        cart[product_id] = {
            'type': 'shoes',
            'name': product.name,
            'price': product.price,
            'size': size,
            'quantity': cart.get(product_id, {}).get('quantity', 0) + 1
        }
        request.session['cart'] = cart

        return redirect('goods:shoe', product_id=product_id)
    
    product = get_object_or_404(Product, id=product_id)
    all_products = Product.objects.all()
    ln_products = len(all_products)
    look_at = []
    for _ in range(4):
        look_at.append(all_products[random.randint(0, ln_products-1)])

    context = {
        'look_at': look_at,
        'product': product
    }

    return render(request, 'catalog/shoes_id.html', context=context)


def clothcart(request, product_id):
    if request.method == 'POST':
        size = request.POST.get('size') 
        product = get_object_or_404(Cloth, id=product_id)
        # print(product)
        
        cart = request.session.get('cart', {})
        cart[product_id] = {
            'type': 'cloth',
            'name': product.name,
            'price': product.price,
            'size': size,
            'quantity': cart.get(product_id, {}).get('quantity', 0) + 1
        }
        request.session['cart'] = cart

        return redirect('goods:shoe', product_id=product_id)
    
    product = get_object_or_404(Cloth, id=product_id)
    all_products = Cloth.objects.all()
    ln_products = len(all_products)
    look_at = []
    for _ in range(4):
        look_at.append(all_products[random.randint(0, ln_products-1)])

    context = {
        'look_at': look_at,
        'product': product
    }

    return render(request, 'catalog/shoes_id.html', context=context)


def view_cart(request):
    code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(5)) + str(int(time.time()))[:-4]

    cart = request.session.get('cart', {})


    cart_items = []
    total_price = 0 
    for product_id, item_data in cart.items():
        # print(cart.items())
        # print(item_data['type'])
        if item_data['type'] == 'shoes':
            product = Product.objects.get(id=product_id)
        else:
            product = Cloth.objects.get(id=product_id)

        item = {
            'product': product,
            'size': item_data['size'],
            'quantity': item_data['quantity'],
            'total_price': item_data['quantity'] * item_data['price'],
            'cart': cart,
            'code': code,
        }
        cart_items.append(item)
        total_price += item['total_price']

    return render(request, 'catalog/cart.html', {'code': code, 'cart_items': cart_items, 'total_price': total_price, 'res_price': total_price + 8000})


# def update_cart(request, product_id, count):
#     if request.method == 'POST':
#         cart = request.session.get('cart', {})
#         quantity = count
#         if product_id in cart:
#             cart[product_id]['quantity'] = count
#             request.session['cart'] = cart

#     return redirect('goods:view_cart')

def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity_' + product_id)  # Уникальный идентификатор для каждого товара
        
        cart = request.session.get('cart', {})
        cart[product_id]['quantity'] = int(quantity)
        request.session['cart'] = cart
        print(cart)

    return redirect('goods:view_cart')


def remove_item_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart

    return redirect('goods:view_cart')


def display_info(request):
    return render(request, 'faq/faq.html')


@csrf_exempt
def order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        
        if cart is not None:
            try:
                code = request.POST.get('code')
                new_order = Order.objects.create(code=code, cart=cart)
                del request.session['cart']

                return JsonResponse({'status': 'success'})
            except json.JSONDecodeError as e:
                return JsonResponse({'error': 'Invalid JSON format for cart data'}, status=400)
        else:
            return JsonResponse({'error': 'No cart data provided in the request'}, status=400)

    return JsonResponse({'error': 'Method Not Allowed'}, status=405)


def delivery(request):
    return render(request, 'faq/delivery.html')

def money(request):
    return render(request, 'faq/money.html')

def money_back(request):
    return render(request, 'faq/money_back.html')