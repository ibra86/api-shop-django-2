from django.db.models import Model, CharField, DecimalField, DO_NOTHING, TextField, ManyToManyField, \
    ForeignKey, IntegerField

from users.models import CustomUser

MAX_NAME_LENGTH = 80


class Shop(Model):
    name = CharField(max_length=MAX_NAME_LENGTH)
    city = CharField(max_length=MAX_NAME_LENGTH)
    owner = CharField(max_length=MAX_NAME_LENGTH)

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=MAX_NAME_LENGTH)
    price = DecimalField(max_digits=6, decimal_places=2)
    category = CharField(max_length=MAX_NAME_LENGTH, blank=True)
    shop_id = ManyToManyField(Shop)
    description = TextField(blank=True)

    def __str__(self):
        return self.name


# class User(Model):
#     user = OneToOneField(CustomUser, on_delete=CASCADE)

class Basket(Model):
    user_id = ForeignKey(CustomUser, on_delete=DO_NOTHING)
    item = ManyToManyField(Product, blank=True, default=None)
    quantity = IntegerField(default=0)

    @property
    def get_quantity_value(self):
        return self.quantity

    def __str__(self):
        return f'Basket with {self.get_quantity_value} items'
