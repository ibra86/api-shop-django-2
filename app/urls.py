from django.urls import path

from app.views import IndexView, ShopListView, ProductListView, ShopCreateView, ProductCreateView, ShopDetailView, \
    ProductShopItemCreateView, BasketCreateView, BasketListView, BuyConfirmTemplateView, BuyAcceptedTemplateView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('shop-list/', ShopListView.as_view(), name='shop-list'),
    path('shop-create/', ShopCreateView.as_view(), name='shop-create'),
    path('shop-detail/<int:pk>', ShopDetailView.as_view(), name='shop-detail'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
    path('product-create/', ProductCreateView.as_view(), name='product-create'),
    path('product-shop-item-create/<int:pk>', ProductShopItemCreateView.as_view(), name='product-shop-item-create'),
    path('basket-list/', BasketListView.as_view(), name='basket-list'),
    path('basket-add/', BasketCreateView.as_view(), name='basket-add'),
    path('buy-confirm/', BuyConfirmTemplateView.as_view(), name='buy-confirm'),
    path('buy-accepted/', BuyAcceptedTemplateView.as_view(), name='buy-accepted'),
]
