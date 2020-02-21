from django.forms import ModelForm

from app.models import ProductShopItem, Shop


class ProductShopItemCreateForm(ModelForm):
    class Meta:
        model = ProductShopItem
        fields = '__all__'

