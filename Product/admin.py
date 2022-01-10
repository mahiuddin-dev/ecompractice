from django.contrib import admin
from django.contrib.admin.decorators import register
from django_summernote.admin import SummernoteModelAdmin
from .models import *

# Register your models here.

admin.site.register([Stock,ProductSize,ProductImages,ProductColorImages,Order,OrderItem,Shipping])

class AdminCategory(admin.ModelAdmin):
    list_display = [
        'CategoryName'
    ]
    prepopulated_fields = {'slug': ['CategoryName', ]}

admin.site.register(Category, AdminCategory)

class AdminProduct(admin.ModelAdmin):
    list_display = [
        "Title",
    ]
    prepopulated_fields = {'slug': ['Title']}

admin.site.register(Product, AdminProduct)
