from django.urls import path

from .views import shoes, index, shoescart

app_name = 'goods'

urlpatterns = [
    path('', index, name='index'),
    path('shoes/', shoes, name='shoes'),
    path('shoes/<int:product_id>', shoescart, name="shoe")
]