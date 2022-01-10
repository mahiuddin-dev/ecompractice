from django.views.generic import TemplateView
from Product.models import Product
# Create your views here.


class HomeView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
   
        products = Product.objects.all().order_by('-id')[:8]

        context['products'] = products
        
        return context

        