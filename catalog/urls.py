from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import HomeListView, ProductDetailView, ContactFeedbackView

app_name = CatalogConfig.name

urlpatterns = [
    path("", HomeListView.as_view(), name="product_list"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product_detail"),
    path("contact/", ContactFeedbackView.as_view(), name="contact"),
]
