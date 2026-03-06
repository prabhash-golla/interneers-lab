import json
from .repository import ProductRepository

class ValidationError(Exception):
    pass

class NotFoundError(Exception):
    pass

def validate_product_data(data: dict):

    if not data.get("name") or not str(data["name"]).strip():
        raise ValidationError("Product 'name' is required and cannot be empty.")
    if not data.get("brand") or not str(data["brand"]).strip():
        raise ValidationError("Product 'brand' is required.")
    
    try:
        price = float(data.get("price", 0))
        if price <= 0:
            raise ValidationError("Product 'price' must be greater than zero.")
    except ValueError:
        raise ValidationError("Product 'price' must be a valid number.")

    try:
        quantity = int(data.get("quantity", 0))
        if quantity < 0:
            raise ValidationError("Product 'quantity' cannot be negative.")
    except ValueError:
        raise ValidationError("Product 'quantity' must be a valid integer.")

def format_product(product) -> dict:
    """Helper to convert the MongoEngine database object back into a standard dictionary."""
    data = json.loads(product.to_json())
    data['id'] = data.pop('_id', {}).get('$oid', str(product.id))
    return data

def create_product(data: dict) -> dict:
    validate_product_data(data)
    
    product = ProductRepository.create(data)
    return format_product(product)

def get_product(product_id: str) -> dict:
    product = ProductRepository.get_by_id(product_id)
    if not product:
        raise NotFoundError(f"Product with ID '{product_id}' not found.")
    return format_product(product)

def list_products(page: int = 1, limit: int = 10) -> dict:
    skip = (page - 1) * limit
    
    products = ProductRepository.get_all(skip=skip, limit=limit)
    total_items = ProductRepository.count_all()
    
    return {
        "items": [format_product(p) for p in products],
        "total": total_items,
        "page": page,
        "limit": limit,
        "total_pages": (total_items + limit - 1) // limit
    }

def update_product(product_id: str, data: dict) -> dict:
    product = ProductRepository.get_by_id(product_id)
    if not product:
        raise NotFoundError(f"Product with ID '{product_id}' not found.")
    
    validate_product_data(data)
    
    updated_product = ProductRepository.update(product, data)
    return format_product(updated_product)

def delete_product(product_id: str) -> dict:
    product = ProductRepository.get_by_id(product_id)
    if not product:
        raise NotFoundError(f"Product with ID '{product_id}' not found.")
    
    ProductRepository.delete(product)
    return {"message": f"Product '{product_id}' deleted successfully."}