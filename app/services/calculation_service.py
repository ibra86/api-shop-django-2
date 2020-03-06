from itertools import product


def get_total_price(basket):
    basket_item_manager = basket.basketitem_set

    # pairs = [(price, quantity)
    #          for basket_item in basket_item_manager
    #          (price, quantity) := (basket_item.product_shop_item.price, basket_item.quantity)]
    total = 0
    if basket_item_manager.get_queryset().exists():
        for basket_item in basket_item_manager.all():
            price = basket_item.product_shop_item.price
            quantity = basket_item.quantity
            total += price * quantity

    return total
