from django.urls import path
from . import views

app_name = 'Wishlist'

urlpatterns = [
    path('', views.Wishlist.as_view(), name='Wishlist'),
]