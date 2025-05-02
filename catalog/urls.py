from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from .views import (
    ProductListView,
    ProductCreateView,
    ProductDetailView,
    ContactFeedbackView,
    ProductUpdateView,
    ProductDeleteView,
    ProductsByCategoryView,
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("product/create/", ProductCreateView.as_view(), name="product_create"),
    path(
        "product/<int:pk>",
        cache_page(60 * 15)(ProductDetailView.as_view()),
        name="product_detail",
    ),
    path("product/<int:pk>/edit", ProductUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete", ProductDeleteView.as_view(), name="product_delete"),
    path("contact/", ContactFeedbackView.as_view(), name="contact"),
    path(
        "category/<slug:category_slug>/",
        ProductsByCategoryView.as_view(),
        name="products_by_category",
    ),
]
