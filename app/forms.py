from django.forms import ModelForm

from app.models import ProductShopItem, Shop


class ProductShopItemCreateForm(ModelForm):
    class Meta:
        model = ProductShopItem
        fields = '__all__'

    # def is_valid(self):
    #     # product_item = self.cleaned_data.get('product_item')
    #     # shops = self.cleaned_data.get('shops')
    #     # self.Meta.model.objects.all()
    #     return super().is_valid()

