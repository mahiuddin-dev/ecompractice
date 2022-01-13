from django.http import JsonResponse
from django.views.generic import TemplateView, View
from hitcount.views import HitCountDetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import json


from .models import *


class Category(TemplateView):
    template_name = 'category.html'

#! Single Product View Class
class ProductView(HitCountDetailView):
    template_name = 'product.html'
    model = Product
    context_object_name = 'product'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = super().get_object() #? Get current object
        totalView = product.hit_count.hits_in_last(minutes=60)  #? Count last 1 hour view    

        # Get similar products
        similar_products = product.Tags.similar_objects()[:5]

        user = self.request.user
        
        if user.is_authenticated:
            order,created = Order.objects.get_or_create(customer=user)
            items = order.orderitem_set.filter(product=product)
 
            if len(items) > 0:
                cartAdd = False
            else:
                cartAdd = True
        else:
            cartAdd = True
        
        context['total'] = totalView     
        context['cartAdd'] = cartAdd 
        context['similar_products'] = similar_products 
        return context
    

class CartProductView(LoginRequiredMixin, View):
    
    def get(self,request):
        if request.user.is_authenticated:
            customer = request.user
            order,created = Order.objects.get_or_create(customer=customer)
            items = order.orderitem_set.all()
            # items = OrderItem.objects.filter(order=order)
        else:
            items = []
        
        context = {'items': items, 'order': order}

        if(len(items) > 0):
            return render(request,'cart.html',context)
        else:
            return render(request,'cart-empty.html')
    
    def post(self,request):
        return render(request,'cart.html')

class CheckoutView(LoginRequiredMixin, View):
    
    def get(self,request):
        if request.user.is_authenticated:
            customer = request.user
            order,created = Order.objects.get_or_create(customer=customer)
            items = order.orderitem_set.all()
            # items = OrderItem.objects.filter(order=order)
        else:
            items = []
        
        context = {'items': items, 'order': order}

        if(len(items) > 0):
            return render(request,'checkout.html',context)
        else:
            return render(request,'cart-empty.html')
    
    def post(self,request):
        return render(request,'checkout.html')


def UpdateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    quantity = data['quantity']
    action = data['action']
    product_color = data['product_color']
    product_size = data['product_size']

    customer = request.user
    product = Product.objects.get(pk=productId)

    order,created = Order.objects.get_or_create(customer=customer, complete=False)
    
    order_item,created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        order_item.quantity = quantity
        order_item.product_color = product_color
        order_item.product_size = product_size
        order_item.save()
    else:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)


        