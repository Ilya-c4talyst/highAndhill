from django.urls import path

from .views import shoes, index, shoescart, view_cart, update_cart, remove_item_from_cart, display_info, order, popular, newest, delivery, sale, clothes, clothcart, money, money_back

app_name = 'goods'

urlpatterns = [
    path('', index, name='index'),
    path('shoes/', shoes, name='shoes'),
    path('clothes/', clothes, name='clothes'),
    path('shoes/<int:product_id>/', shoescart, name="shoe"),
    path('clothes/<int:product_id>/', clothcart, name="cloth"),
    path('shoes/add_to_cart/<int:product_id>/', shoescart, name='add_to_cart'),
    path('clothes/add_to_cart/<int:product_id>/', clothcart, name='clothes_add_to_cart'),
    path('view_cart/', view_cart, name='view_cart'),
    path('update_cart/', update_cart, name='update_cart'),
    path('remove_item_from_cart/', remove_item_from_cart, name='remove_item_from_cart'),
    path('order/', order, name='order'),

    path('popular/', popular, name='popular'),
    path('new/', newest, name='new'),
    path('sale/', sale, name='sale'),

    path('faq/', display_info, name='faq'),
    path('delivery/', delivery, name='delivery'),
    path('payment/', money, name='payment'),
    path('return-info/', money_back, name='return')

]