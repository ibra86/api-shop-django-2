from django.forms import ModelForm

from app.models import ProductShopItem


class ProductShopItemCreateForm(ModelForm):
    ...
#     class Meta:
#         model = ProductShopItem
#         fields = ('product',)
#
#     def __init__(self, *args, **kwargs):
#         self.shop = kwargs.pop('shop')
#         super().__init__(*args, **kwargs)
#         self.fields['product'].queryset = self.model.objects.filter(user='shop')