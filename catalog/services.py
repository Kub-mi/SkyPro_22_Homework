from django.db.models import QuerySet
from .models import Product

def get_products_by_category(category_id: int) -> QuerySet[Product]:
    return (
        Product.objects
        .select_related("category")   # оптимизация JOIN категории
        .filter(category_id=category_id)
    )