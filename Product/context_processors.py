from .models import *


def CartProductView(request):
    try:
        if request.user.is_authenticated:
            customer = request.user
            order,created = Order.objects.get_or_create(customer=customer)
            items = order.orderitem_set.all()
            has = True
        else:
            has = False
            items = []
        
        context = {'items': items, 'order': order, 'totalorder': len(items),'has':has}
        return context

    except Exception:
        has = False
        items = []
        context = {'items': '','has':has,'totalorder': len(items)}
        return context
    