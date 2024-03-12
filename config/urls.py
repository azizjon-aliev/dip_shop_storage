from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


def redirect_to_admin_page(request):
    from django.shortcuts import redirect
    return redirect('/admin/')


urlpatterns = [
    path('', redirect_to_admin_page),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
