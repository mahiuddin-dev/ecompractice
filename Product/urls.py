from django.urls import path
from . import views

app_name = 'Product'

urlpatterns = [
    path('', views.Category.as_view(), name='Category'),
    path('<str>/<slug>/', views.ProductView.as_view(), name='ProductDetail'),
]