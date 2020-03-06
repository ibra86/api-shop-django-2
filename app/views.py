# Create your views here.
from django.contrib.auth.decorators import permission_required
from django.db.models import F
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, CreateView, DetailView

from app.forms import ProductShopItemCreateForm
from app.models import Basket, Shop, Product, ProductShopItem, BasketItem
from app.services.email_service import send_email_buying_confirmation


class IndexView(TemplateView):
    template_name = "index.html"


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
        pk = self.kwargs.get('pk')
        context['product_shop_items'] = Shop.objects.get(pk=pk).productshopitem_set.all()
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
        initial.update({'shop': Shop.objects.filter(id=shop_id).first()})
        return initial

    def form_valid(self, form):
        product = form.cleaned_data.get('product')
        quantity = form.cleaned_data.get('quantity')

        shop_id = self.kwargs.get('pk')
        obj = ProductShopItem.objects.filter(shops__id=shop_id).filter(product=product)
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
    model = BasketItem
    fields = ('quantity',)
    template_name = 'basket_add.html'

    def form_valid(self, form):
        get_user = self.request.user
        get_product_shop_item_id = self.request.GET.get('product_shop_item_id')
        get_quantity = form.instance.quantity

        product_shop_item_quantity = ProductShopItem.objects.get(id=get_product_shop_item_id).quantity
        if product_shop_item_quantity <= get_quantity:
            return super().form_invalid(form)

        objs = BasketItem.objects.filter(product_shop_item=get_product_shop_item_id)

        if objs.exists():
            objs.update(quantity=F('quantity') + get_quantity)
        else:
            basket_item = BasketItem(
                basket=Basket.objects.get(user=get_user),
                product_shop_item=ProductShopItem.objects.get(id=get_product_shop_item_id),
                quantity=get_quantity
            )
            basket_item.save()

        ProductShopItem.objects.filter(id=get_product_shop_item_id).update(quantity=F('quantity') - get_quantity)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('shop-detail', kwargs={'pk': self.request.GET.get('shop_id')})


class BasketListView(ListView):
    template_name = 'basket_list.html'
    context_object_name = 'basket_items'
    model = BasketItem

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket_total_price'] = Basket.objects.get(user=self.request.user).total_price
        return context


class BuyConfirmTemplateView(TemplateView):
    template_name = 'buy_confirm.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket_total_price'] = Basket.objects.get(user=self.request.user).total_price
        return context


class BuyAcceptedTemplateView(TemplateView):
    template_name = 'buy_accepted.html'

    def get_context_data(self, **kwargs): # TODO change method for more appropriate
        send_email_buying_confirmation()
        BasketItem.objects.filter(basket__user=self.request.user).delete()
        return super().get_context_data(**kwargs)
