from typing import List
from django.conf import settings
from django.core.cache import cache
from django.db.models import QuerySet
from .models import Product

def get_products_by_category(category_id: int) -> QuerySet[Product]:
    return (
        Product.objects
        .select_related("category")   # оптимизация JOIN категории
        .filter(category_id=category_id)
    )

CACHE_VER = "v1"  # на случай изменения формата ключей

def _category_ids_cache_key(category_id: int) -> str:
    return f"cat:{category_id}:ids:{CACHE_VER}"

def get_category_product_ids(category_id: int) -> List[int]:
    """
    Низкоуровневое кеширование: возвращаем упорядоченный список ID товаров категории.
    Кешируем только IDs — это компактно и универсально.
    """
    key = _category_ids_cache_key(category_id)
    ids = cache.get(key)
    if ids is not None:
        return ids

    # Базовый порядок — по id
    ids = list(
        Product.objects
        .filter(category_id=category_id)
        .order_by("id")
        .values_list("id", flat=True)
    )
    cache.set(key, ids, getattr(settings, "PRODUCT_LIST_CACHE_TTL", 300))
    return ids

def get_products_by_ids_preserving_order(ids: List[int]) -> QuerySet[Product]:
    """
    Возвращает QuerySet продуктов по списку IDs, С СОХРАНЕНИЕМ ПОРЯДКА ids.
    """
    if not ids:
        return Product.objects.none()
    from django.db.models import Case, When, IntegerField
    preserved = Case(
        *[When(pk=pk, then=pos) for pos, pk in enumerate(ids)],
        output_field=IntegerField()
    )
    return (
        Product.objects
        .select_related("category")
        .filter(id__in=ids)
        .order_by(preserved)
    )
