# django_app/repository.py
from .models import Product,ProductCategory
from mongoengine.errors import DoesNotExist


class ProductCategoryRepository:
    @staticmethod
    def create(data: dict) -> ProductCategory:
        category = ProductCategory(**data)
        category.save()
        return category

    @staticmethod
    def get_by_id(category_id: str) -> ProductCategory:
        try:
            return ProductCategory.objects.get(id=category_id)
        except DoesNotExist:
            return None

    @staticmethod
    def get_all():
        return ProductCategory.objects.all()

    @staticmethod
    def delete(category: ProductCategory):
        category.delete()

class ProductRepository:
    @staticmethod
    def create(data: dict) -> Product:
        product = Product(**data)
        product.save()
        return product

    @staticmethod
    def get_by_id(product_id: str) -> Product:
        try:
            return Product.objects.get(id=product_id)
        except DoesNotExist:
            return None

    @staticmethod
    def get_all(skip: int = 0, limit: int = 10):
        return Product.objects.skip(skip).limit(limit)

    @staticmethod
    def count_all() -> int:
        return Product.objects.count()

    @staticmethod
    def update(product: Product, data: dict) -> Product:
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product

    @staticmethod
    def delete(product: Product):
        product.delete()

    @staticmethod
    def get_by_category(category: ProductCategory):
        return Product.objects.filter(category=category)