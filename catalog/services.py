from django.core.cache import cache

from config.settings import CACHE_ENABLED
from .models import Product, Category


def get_products_by_category(category_slug):
    """
    Возвращает список продуктов в указанной категории с кешированием
    """
    cache_key = f"products_category_{category_slug}"
    cached_products = cache.get(cache_key)

    if cached_products is not None:
        return cached_products

    try:
        category = Category.objects.get(slug=category_slug)
        products = list(
            Product.objects.filter(category=category).select_related("category")
        )
        cache.set(cache_key, products, 3600)  # Кешируем на 1 час
        return products
    except Category.DoesNotExist:
        return []


def get_product_from_cache():
    """Получает данные по продуктам из кэша, если кэш пуст, получает данные из БД"""
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = "product_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products
