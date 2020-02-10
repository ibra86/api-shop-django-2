from django.db.models import Model, CharField, EmailField, DecimalField, DO_NOTHING, TextField, ManyToManyField, \
    ForeignKey, OneToOneField, CASCADE, IntegerField

from users.models import CustomUser

MAX_NAME_LENGTH = 80


class User(Model):
    user = OneToOneField(CustomUser, on_delete=CASCADE)
    name = CharField(max_length=MAX_NAME_LENGTH)
    email = EmailField(null=True)


class Shop(Model):
    name = CharField(max_length=MAX_NAME_LENGTH)
    city = CharField(max_length=MAX_NAME_LENGTH)
    owner = CharField(max_length=MAX_NAME_LENGTH)

    def __str__(self):
        return self.name


class Item(Model):
    name = CharField(max_length=MAX_NAME_LENGTH)
    price = DecimalField(max_digits=6, decimal_places=2)
    category = CharField(max_length=MAX_NAME_LENGTH, blank=True)
    shop_id = ManyToManyField(Shop)
    description = TextField(blank=True)

    def __str__(self):
        return self.name


class Basket(Model):
    user_id = ForeignKey(User, on_delete=DO_NOTHING)
    item = ManyToManyField(Item)
    quantity = IntegerField()

    def __str__(self):
        return self.name

