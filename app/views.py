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
    template_name = "shop_detail.html"
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

    # success_url = reverse_lazy('shop-list')

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['shop_id'] = self.request.resolver_match.kwargs.get('pk')
    #     return kwargs

    def get_initial(self):
        initial = super().get_initial()
        shop_id = self.kwargs.get('pk')
        initial.update({'shops': Shop.objects.filter(id=shop_id).first()})
        return initial

    def form_valid(self, form):
        product_item = form.cleaned_data.get('product_item')
        shops = form.cleaned_data.get('shops').first()
        quantity = form.cleaned_data.get('quantity')

        shop_id = self.kwargs.get('pk')
        obj = ProductShopItem.objects.filter(shops__id=shop_id).filter(product_item=product_item)
        if not obj.exists():
            return super().form_valid(form)

        quantity += obj.first().quantity
        obj.update(quantity=quantity)
        return HttpResponseRedirect(self.get_success_url())

            # obj
        # if ProductShopItem.objects.filter(product_item=product_item).filter(shops=shops).exists():
        #     form.errors.update({'my_error': True})
        # return super().form_invalid(form)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shop_id'] = self.kwargs.get('pk')
        return context

    def get_success_url(self):
        return reverse_lazy('shop-detail', kwargs={'pk': self.kwargs.get('pk')})
