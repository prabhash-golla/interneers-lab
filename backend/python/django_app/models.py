# django_app/models.py
import datetime
from mongoengine import Document, StringField, FloatField, IntField, DateTimeField ,ReferenceField

class ProductCategory(Document):
    title = StringField(required=True, unique=True)
    description = StringField(default="")
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'product_categories'}

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()
        return super(ProductCategory, self).save(*args, **kwargs)

class Product(Document):
    name = StringField(required=True)
    description = StringField(default="")
    # category = StringField(default="Uncategorized")
    category = ReferenceField(ProductCategory, null=True)
    price = FloatField(required=True, min_value=0.01)
    brand = StringField(required=True)
    quantity = IntField(required=True, min_value=0)
    
    # Advanced Goal: Audit Columns
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'products'}

    def save(self, *args, **kwargs):
        """Override save to automatically update the 'updated_at' timestamp."""
        if not self.id:
            self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()
        return super(Product, self).save(*args, **kwargs)