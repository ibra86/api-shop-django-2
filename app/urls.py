from django.urls import path

from app.views import IndexView, ShopListView, ProductListView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('shop-list/', ShopListView.as_view(), name='shop-list'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('basket-list/', ProductListView.as_view(), name='basket-list'),
]
