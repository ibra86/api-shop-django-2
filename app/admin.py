from django.contrib import admin

from app.models import Product, Shop, Basket

admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(Basket)
