# Create your views here.
from django.views.generic import TemplateView, ListView

from app.models import Basket, Shop, Product


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            basket = Basket(user_id=self.request.user)
            basket.save()
            context['basket'] = basket
        return context

class ShopListView(ListView):
    template_name = "shop_list.html"
    model = Shop
    # context_object_name = 'persons'

class ProductListView(ListView):
    template_name = "shop_list.html"
    model = Product