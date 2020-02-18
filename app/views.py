# Create your views here.
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView, DetailView

from app.forms import ProductShopItemCreateForm
from app.models import Basket, Shop, Product, ProductShopItem


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
    template_name = 'shop_list.html'
    context_object_name = 'objects'
    model = Shop


class ShopDetailView(DetailView):
    template_name = "shop_detail.html"
    model = Shop

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_shop_items'] = ProductShopItem.objects.filter(shop_id=self.kwargs.get('pk'))
        return context


class ShopCreateView(CreateView):
    model = Shop
    fields = '__all__'
    success_url = reverse_lazy('shop-list')
    template_name = 'shop_create.html'

    @method_decorator(permission_required('app.view_shop', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductListView(ListView):
    template_name = 'product_list.html'
    context_object_name = 'objects'
    model = Product


class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('product-list')
    template_name = 'product_create.html'

    @method_decorator(permission_required('app.view_product', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductShopItemCreateView(CreateView):
    ...
    # # model = ProductShopItem
    # # fields = '__all__'
    # form_class = ProductShopItemCreateForm
    #
    # # def get_form_kwargs(self):
    # #     kwargs = super(FolderCreate, self).get_form_kwargs()
    # #     kwargs['user'] = self.request.user
    # #     return kwargs
    #
    # # success_url = reverse_lazy('shop-detail')
    # template_name = 'product_shop_item_create.html'
    # #
    # # def get_success_url(self):
    # #     return reverse_lazy('shop-detail', kwargs={'pk': self.object.pk})
