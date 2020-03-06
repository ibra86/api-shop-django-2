from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db.models import Model, CharField, DecimalField, DO_NOTHING, TextField, ManyToManyField, \
    ForeignKey, IntegerField, PositiveIntegerField, CASCADE, OneToOneField, ImageField

from app.services.calculation_service import get_total_price
from users.models import CustomUser

MAX_NAME_LENGTH = 80


class Shop(Model):
    name = CharField(max_length=MAX_NAME_LENGTH, unique=True)
    city = CharField(max_length=MAX_NAME_LENGTH)
    owner = CharField(max_length=MAX_NAME_LENGTH)
    # budget = DecimalField(decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], default=1_000)

    class Meta:
        verbose_name = 'M1_Shop'

    def __str__(self):
        return f'Shop - {self.name} ({self.city})'


class Product(Model):
    name = CharField(max_length=MAX_NAME_LENGTH, unique=True)
    category = CharField(max_length=MAX_NAME_LENGTH, blank=True)
    description = TextField(blank=True)
    picture = ImageField(upload_to='product', help_text='product\'s image', blank=True)
    shops = ManyToManyField(Shop, through='ProductShopItem')

    class Meta:
        verbose_name = 'M2_Product'

    def __str__(self):
        return f'Product - {self.name} ({self.category})'


class ProductShopItem(Model):
    product = ForeignKey(Product, on_delete=DO_NOTHING)
    shop = ForeignKey(Shop, on_delete=DO_NOTHING)
    quantity = PositiveIntegerField(default=1)
    price = DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        verbose_name = 'M3_ProductShopItem'
        unique_together = ('product', 'shop')

    def __str__(self):
        return f'Item [{self.product}, {self.shop})] - {self.quantity} pcs.'


class Basket(Model):
    user = OneToOneField(CustomUser, on_delete=DO_NOTHING)

    @property
    def total_price(self):
        return get_total_price(self)

    class Meta:
        verbose_name = 'M4_Basket'

    def __str__(self):
        return f'Basket [user - {self.user}, total_price = {self.total_price}]'


class BasketItem(Model):
    basket = ForeignKey(Basket, on_delete=CASCADE)
    product_shop_item = OneToOneField(ProductShopItem, on_delete=DO_NOTHING)
    quantity = PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'M5_BasketItem'
        unique_together = ('basket', 'product_shop_item')

    def __str__(self):
        return f'BasketItem [{self.basket}, {self.product_shop_item})] - {self.quantity} pcs.'