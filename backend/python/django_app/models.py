# django_app/models.py
import datetime
from mongoengine import Document, StringField, FloatField, IntField, DateTimeField

class Product(Document):
    name = StringField(required=True)
    description = StringField(default="")
    category = StringField(default="Uncategorized")
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