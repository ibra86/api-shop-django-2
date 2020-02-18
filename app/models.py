from django.db.models import Model, CharField, DecimalField, DO_NOTHING, TextField, ManyToManyField, \
    ForeignKey, IntegerField

from users.models import CustomUser

MAX_NAME_LENGTH = 80


class Shop(Model):
    name = CharField(max_length=MAX_NAME_LENGTH, unique=True)
    city = CharField(max_length=MAX_NAME_LENGTH)
    owner = CharField(max_length=MAX_NAME_LENGTH)


class Product(Model):
    name = CharField(max_length=MAX_NAME_LENGTH, unique=True)
    price = DecimalField(max_digits=6, decimal_places=2)
    category = CharField(max_length=MAX_NAME_LENGTH, blank=True)
    description = TextField(blank=True)


class ProductShopItem(Model):
    product = ForeignKey(Product, on_delete=DO_NOTHING)
    shop = ManyToManyField(Shop)

    def __str__(self):
        # return self.name
        return f'Products {self.product.name}'


class Basket(Model):
    user = ForeignKey(CustomUser, on_delete=DO_NOTHING)
    item = ManyToManyField(Product, blank=True, default=None)
    quantity = IntegerField(default=0)

    @property
    def get_quantity_value(self):
        return self.quantity

    def __str__(self):
        return f'Basket with {self.get_quantity_value} items'
