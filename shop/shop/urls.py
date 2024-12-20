from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from shop import settings

urlpatterns = [
    path('', include('goods.urls', namespace='goods')),
    path('admin/', admin.site.urls),
]



if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)