from django.db.models import Sum

from app.models import Basket


def basket_init(request):
    basket_items = None
    if request.user.is_authenticated:
        user = request.user
        basket_items = Basket.objects.filter(user=user).aggregate(Sum('quantity')).get('quantity__sum')
    basket_items = int(0 if basket_items is None else basket_items)
    return {"basket_items": basket_items}
