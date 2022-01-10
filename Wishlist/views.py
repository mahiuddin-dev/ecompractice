from django.views.generic import TemplateView

# Create your views here.

class Wishlist(TemplateView):
    template_name = 'account-wishlist.html'


