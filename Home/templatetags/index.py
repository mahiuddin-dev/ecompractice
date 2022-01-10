from django import template
from django.template.defaulttags import register
register = template.Library()


@register.filter
def finalprice(Price,Percentage):
    return int((int(Price) - (int(Price)*(int(Percentage)/100))))

@register.filter
def SaveMoney(OldPrice,PercentagePrice):
    return int(OldPrice) - finalprice(OldPrice,PercentagePrice)

