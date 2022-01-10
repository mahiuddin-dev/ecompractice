from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve as mediaserve

from Product.views import CartProductView,CheckoutView,UpdateItem


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls', namespace='Home')),
    path('Category/', include('Product.urls', namespace='Product')),
    path('Wishlist/', include('Wishlist.urls', namespace='Wishlist')),
    path('Account/', include('Authentication.urls', namespace='Authentication')),
    path('Cart/', CartProductView.as_view(), name='cart_page'),
    path('Checkout/', CheckoutView.as_view(), name='checkout_page'),
    path('update_item/', UpdateItem, name='update_item'),
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


urlpatterns.append(url(f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$',
        mediaserve,
        {'document_root': settings.MEDIA_ROOT}))

urlpatterns += staticfiles_urlpatterns()
