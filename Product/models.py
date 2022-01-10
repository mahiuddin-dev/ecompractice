from typing import ItemsView
from django.db import models
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User

from hitcount.settings import MODEL_HITCOUNT
from hitcount.models import HitCountMixin
# Create your models here.


class Category(models.Model):
    CategoryName = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.CategoryName

class Stock(models.Model):
    stock = models.CharField(max_length=50, default='Available')
    def __str__(self):
        return self.stock

class Product(models.Model,HitCountMixin):
    Name = models.CharField(max_length=250)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    Product_label = models.CharField(max_length=50, default='New')
    Price = models.PositiveIntegerField()
    Tags = TaggableManager()
    DiscountPercentage = models.IntegerField(default=0)
    PromoCode = models.CharField(max_length=50, null=True, blank=True)
    PromoDiscount = models.PositiveIntegerField(default=0)
    Stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    Wrranty = models.CharField(max_length=250, null =True, blank = True)
    ReturnPolicy = models.CharField(max_length=300, null=True, blank = True)
    ShortDescription = models.TextField()
    Description = models.TextField()
    Images = models.ImageField(upload_to="Products")
    ViewCount = models.PositiveIntegerField(default=0)
    hit_count_generic = GenericRelation(MODEL_HITCOUNT, object_id_field='object_pk',
    related_query_name='hit_count_generic_relation')

    def __str__(self):
        return self.Title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('Product:ProductDetail', kwargs={'str' : self.Category, 'slug': self.slug})

class ProductColorImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="Product/Color/images")
    Color_Name = models.CharField(max_length=50)

    def __str__(self):
        return self.product.Title

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="Product/images")
   
    def __str__(self):
        return self.product.Title

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size_name = models.CharField(max_length=50)
    length = models.CharField(max_length=50,null =True, blank = True)
    Chest = models.CharField(max_length=50,null =True, blank = True)
    size = models.CharField(max_length=50,null =True, blank = True)

    def __str__(self):
        return self.product.Title+'... Product size -> '+self.size_name


# Order model
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, null =True, blank = True)

    def __str__(self):
        return str(self.customer.username)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
 
        return total

# Order Item model
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, blank=True, null = True)
    product_color = models.CharField(max_length=50, blank=True, null = True)
    product_size = models.CharField(max_length=50, blank=True, null = True)
    order_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order)+ " => "+self.product.Title
    
    @property
    def get_total(self):
        total = 0
        if self.product.DiscountPercentage > 0:
            actual = self.product.Price - (self.product.Price*self.product.DiscountPercentage)/100
            total += self.quantity * actual
        else:
            total += self.quantity * self.product.Price

        return total


# Shipping model
class Shipping(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null = True, blank = True)
    city = models.CharField(max_length=200, null = True, blank = True)
    state = models.CharField(max_length=200, null = True, blank = True)
    zipcode = models.CharField(max_length=200, null = True, blank = True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address