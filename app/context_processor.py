from django.db.models import Sum

from app.models import Basket


def basket_init(request):
    b = None
    if request.user.is_authenticated:
        user = request.user
        b = Basket.objects.get_or_create(user=user)[0]
        b = b.basketitem_set.aggregate(Sum('quantity'))
        b = b.get('quantity__sum')
    basket_items_total = int(0 if b is None else b)
    return {"basket_items_total": basket_items_total}
