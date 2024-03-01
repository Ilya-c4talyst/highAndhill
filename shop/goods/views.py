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


from .models import Product, Brand, Banner, Size, Type, Order


def index(request):
    products = Product.objects.all()
    type = get_object_or_404(Type, name="main")
    banners = type.banners.all()
    ln = len(banners)
    banner = banners[random.randint(0, ln-1)]
    context = {
        "products": products,
        'banner': banner
    }
    return render(request, 'index.html', context=context)


def shoes(request):
    products = Product.objects.all()
    brands = Brand.objects.all()
    sizes = Size.objects.all()

    type = get_object_or_404(Type, name="shoes")
    banners = type.banners.all()
    ln = len(banners)
    info = []
    for _ in range(3):
        info.append(banners[random.randint(0, ln-1)])
    
    search_query = request.GET.get('search_query')

    if search_query:
        products = products.filter(name__icontains=search_query)

    selected_brand = request.GET.get('brand')
    if selected_brand:
        products = products.filter(brand__id=selected_brand)

    selected_size = request.GET.get('sizes')
    if selected_size:
        products = products.filter(sizes__id=selected_size)


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


def shoescart(request, product_id):
    if request.method == 'POST':
        size = request.POST.get('size') 
        product = get_object_or_404(Product, id=product_id)
        
        cart = request.session.get('cart', {})
        print(cart)
        cart[product_id] = {
            'name': product.name,
            'price': product.price,
            'size': size,
            'quantity': cart.get(product_id, {}).get('quantity', 0) + 1
        }
        request.session['cart'] = cart
        
        messages.success(request, 'Товар успешно добавлен в корзину!')
        return redirect('goods:shoe', product_id=product_id)
    
    product = get_object_or_404(Product, id=product_id)
    all_products = Product.objects.all()
    ln_products = len(all_products)
    look_at = []
    for _ in range(3):
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
        product = Product.objects.get(id=product_id)
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


def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')

        cart = request.session.get('cart', {})
        if product_id in cart:
            cart[product_id]['quantity'] = int(quantity)
            request.session['cart'] = cart

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