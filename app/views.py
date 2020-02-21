# Create your views here.
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
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
            # TODO
            # Basket.objects.filter(user=self.request.user).exists()
            # basket = Basket(user=self.request.user)
            # # basket = Basket.objects.filter(user=self.request.user)
            # basket.save()
            basket = 0
            context['basket'] = basket
        return context


class ShopListView(ListView):
    template_name = 'shop_list.html'
    context_object_name = 'objects'
    model = Shop


class ShopDetailView(DetailView):
    template_name = 'shop_detail.html'
    context_object_name = 'shop'
    model = Shop

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_shop_items'] = ProductShopItem.objects.filter(shops__id=self.kwargs.get('pk'))
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
    form_class = ProductShopItemCreateForm
    template_name = 'product_shop_item_create.html'

    def get_initial(self):
        initial = super().get_initial()
        shop_id = self.kwargs.get('pk')
        initial.update({'shops': Shop.objects.filter(id=shop_id).first()})
        return initial

    def form_valid(self, form):
        product_item = form.cleaned_data.get('product_item')
        quantity = form.cleaned_data.get('quantity')

        shop_id = self.kwargs.get('pk')
        obj = ProductShopItem.objects.filter(shops__id=shop_id).filter(product_item=product_item)
        if not obj.exists():
            return super().form_valid(form)

        quantity += obj.first().quantity
        obj.update(quantity=quantity)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_id'] = self.kwargs.get('pk')
        return context

    def get_success_url(self):
        return reverse_lazy('shop-detail', kwargs={'pk': self.kwargs.get('pk')})


class BasketCreateView(CreateView):
    model = Basket
    fields = ('quantity',)
    template_name = 'basket_add.html'

    # def form_valid(self, form):
    #     user = self.request.user
    #     product_shop_item_id = self.request.GET.get('product_shop_item_id')
    #     item = ProductShopItem.objects.get(id=product_shop_item_id)
    #     quantity = form.fields.get('quantity')
    #     basket = form.instance
    #     basket2 = Basket()
    #     # basket = Basket(user=user, quantity=quantity)
    #     # basket.add(item=item)
    #     form.instance = basket
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        kwargs
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy('shop-detail', kwargs={'pk': self.kwargs.get('pk')})
