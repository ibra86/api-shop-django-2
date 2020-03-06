from django.contrib import admin

from app.models import Product, Shop, Basket, ProductShopItem, BasketItem

admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(ProductShopItem)
admin.site.register(Basket)
admin.site.register(BasketItem)
