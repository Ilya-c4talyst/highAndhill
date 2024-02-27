from django.shortcuts import render, get_object_or_404, redirect

from django.contrib import messages

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


# def shoescart(requeset, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     all = Product.objects.all()
#     ln_products = len(all)
#     look_at = []
#     for _ in range(3):
#         look_at.append(all[random.randint(0, ln_products-1)])

#     context = {
#         'look_at': look_at,
#         'product': product
#     }

#     return render(requeset, 'catalog/shoes_id.html', context=context)


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


# def view_cart(request):
#     cart = request.session.get('cart', {})
#     cart_items = []

#     for product_id, item_data in cart.items():
#         product = Product.objects.get(id=product_id)
#         item = {
#             'product': product,
#             'size': item_data['size'],
#             'quantity': item_data['quantity'],
#             'total_price': item_data['quantity'] * item_data['price']
#         }
#         cart_items.append(item)

#     return render(request, 'catalog/cart.html', {'cart_items': cart_items})


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []

    total_price = 0  # Инициализируем переменную для общей стоимости корзины

    for product_id, item_data in cart.items():
        product = Product.objects.get(id=product_id)
        item = {
            'product': product,
            'size': item_data['size'],
            'quantity': item_data['quantity'],
            'total_price': item_data['quantity'] * item_data['price']
        }
        cart_items.append(item)
        total_price += item['total_price']  # Увеличиваем общую стоимость на стоимость текущего товара

    return render(request, 'catalog/cart.html', {'cart_items': cart_items, 'total_price': total_price})


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
