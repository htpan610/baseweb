from django.urls import path

from .views import ProductFilterSchemaView,ProductListView
urlpatterns = [
    path('products/filters/',ProductFilterSchemaView.as_view(),name="product-filters"),
    path('products/',ProductListView.as_view(),name="product-list"),
]
