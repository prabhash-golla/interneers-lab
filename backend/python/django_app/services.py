import uuid
from dataclasses import dataclass, asdict
from typing import Dict

@dataclass
class Product:
    id: str
    name: str
    description: str
    category: str
    price: float
    brand: str
    quantity: int

PRODUCTS_DB: Dict[str, Product] = {}

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

def create_product(data: dict) -> dict:
    validate_product_data(data)
    
    product_id = str(uuid.uuid4())
    new_product = Product(
        id=product_id,
        name=data["name"],
        description=data.get("description", ""),
        category=data.get("category", "Uncategorized"),
        price=float(data["price"]),
        brand=data["brand"],
        quantity=int(data["quantity"])
    )
    
    PRODUCTS_DB[product_id] = new_product
    return asdict(new_product)

def get_product(product_id: str) -> dict:
    product = PRODUCTS_DB.get(product_id)
    if not product:
        raise NotFoundError(f"Product with ID '{product_id}' not found.")
    return asdict(product)

def list_products(page: int = 1, limit: int = 10) -> dict:
    all_products = list(PRODUCTS_DB.values())
    total_items = len(all_products)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    
    paginated_products = all_products[start_idx:end_idx]
    
    return {
        "items": [asdict(p) for p in paginated_products],
        "total": total_items,
        "page": page,
        "limit": limit,
        "total_pages": (total_items + limit - 1) // limit
    }

def update_product(product_id: str, data: dict) -> dict:
    if product_id not in PRODUCTS_DB:
        raise NotFoundError(f"Product with ID '{product_id}' not found.")
    
    validate_product_data(data)
    
    updated_product = Product(
        id=product_id,
        name=data["name"],
        description=data.get("description", ""),
        category=data.get("category", "Uncategorized"),
        price=float(data["price"]),
        brand=data["brand"],
        quantity=int(data["quantity"])
    )
    
    PRODUCTS_DB[product_id] = updated_product
    return asdict(updated_product)

def delete_product(product_id: str) -> dict:
    if product_id not in PRODUCTS_DB:
        raise NotFoundError(f"Product with ID '{product_id}' not found.")
    
    del PRODUCTS_DB[product_id]
    return {"message": f"Product '{product_id}' deleted successfully."}