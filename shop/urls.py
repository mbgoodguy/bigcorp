from django.urls import path

from shop.views import ProductListView, products_detail_view, category_list, search_products

app_name = 'shop'

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('search_products/', search_products, name='search_products'),
    path('<slug:slug>/', products_detail_view, name='products_detail'),
    path('search/<slug:slug>/', category_list, name='category_list'),
]
