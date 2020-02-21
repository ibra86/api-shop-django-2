from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db.models import Model, CharField, DecimalField, DO_NOTHING, TextField, ManyToManyField, \
    ForeignKey, IntegerField, PositiveIntegerField

from users.models import CustomUser

MAX_NAME_LENGTH = 80


class Shop(Model):
    name = CharField(max_length=MAX_NAME_LENGTH, unique=True)
    city = CharField(max_length=MAX_NAME_LENGTH)
    owner = CharField(max_length=MAX_NAME_LENGTH)

    def __str__(self):
        return f'Shop[{self.name} ({self.city})]'


class Product(Model):
    name = CharField(max_length=MAX_NAME_LENGTH, unique=True)
    price = DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    category = CharField(max_length=MAX_NAME_LENGTH, blank=True)
    description = TextField(blank=True)

    def __str__(self):
        return f'Product[{self.name} ({self.category}) - {self.price}]$'


class ProductShopItem(Model):
    product_item = ForeignKey(Product, on_delete=DO_NOTHING)
    shops = ManyToManyField(Shop)
    quantity = PositiveIntegerField(default=1)

    def __str__(self):
        # return self.name
        return f'Item[{self.product_item.name} ({self.product_item.category})] - {self.quantity} pcs.'


class Basket(Model):
    user = ForeignKey(CustomUser, on_delete=DO_NOTHING)
    item = ManyToManyField(Product, blank=True, default=None)
    quantity = IntegerField(default=0)

    @property
    def get_quantity_value(self):
        return self.quantity

    def __str__(self):
        return f'Basket - {self.get_quantity_value} items'
