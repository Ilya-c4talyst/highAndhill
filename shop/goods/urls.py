from django.urls import path

from .views import catalog, index

app_name = 'goods'

urlpatterns = [
    path('', index, name='index'),
    path('catalog/', catalog, name='catalog'),
]