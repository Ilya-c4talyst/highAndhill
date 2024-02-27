from django.urls import path

from .views import shoes, index, shoescart, view_cart, update_cart, remove_item_from_cart

app_name = 'goods'

urlpatterns = [
    path('', index, name='index'),
    path('shoes/', shoes, name='shoes'),
    path('shoes/<int:product_id>/', shoescart, name="shoe"),
    path('add_to_cart/<int:product_id>/', shoescart, name='add_to_cart'),
    path('view_cart/', view_cart, name='view_cart'),
    path('update_cart/', update_cart, name='update_cart'),
    path('remove_item_from_cart/', remove_item_from_cart, name='remove_item_from_cart'),

]