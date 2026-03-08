import json
import csv
import io
from .repository import ProductRepository,ProductCategoryRepository
from mongoengine.errors import ValidationError as MongoValidationError

class ValidationError(Exception):
    pass

class NotFoundError(Exception):
    pass

def create_category(data: dict) -> dict:
    if not data.get("title") or not str(data["title"]).strip():
        raise ValidationError("Category 'title' is required.")
    
    category = ProductCategoryRepository.create(data)
    return format_product(category) 

def list_categories() -> list:
    categories = ProductCategoryRepository.get_all()
    return [format_product(c) for c in categories]

def get_category(category_id: str) -> dict:
    category = ProductCategoryRepository.get_by_id(category_id)
    if not category:
        raise NotFoundError(f"Category '{category_id}' not found.")
    return format_product(category)

def delete_category(category_id: str) -> dict:
    category = ProductCategoryRepository.get_by_id(category_id)
    if not category:
        raise NotFoundError(f"Category '{category_id}' not found.")
    
    ProductCategoryRepository.delete(category)
    return {"message": "Category deleted successfully."}

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
    data = json.loads(product.to_json())
    data['id'] = data.pop('_id', {}).get('$oid', str(product.id))
    return data

def create_product(data: dict) -> dict:
    validate_product_data(data)
    
    category_name = data.get('category')
    category_obj = ProductCategoryRepository.get_by_name(category_name)
    if not category_obj:
        raise ValidationError(f"Category '{category_name}' does not exist.")
    data['category'] = category_obj

    try:
        product = ProductRepository.create(data)
        return format_product(product)
    except MongoValidationError as e:
        raise ValidationError(f"Database validation failed: {str(e)}")

def get_product(product_id: str) -> dict:
    product = ProductRepository.get_by_id(product_id)
    if not product:
        raise NotFoundError(f"Product with ID '{product_id}' not found.")
    return format_product(product)

def list_products(page: int = 1, limit: int = 10) -> dict:
    page = max(1, page)
    limit = max(1, limit)
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

def list_products_by_category(category_id: str) -> list:
    category = ProductCategoryRepository.get_by_id(category_id)
    if not category:
        raise NotFoundError(f"Category '{category_id}' not found.")
        
    products = ProductRepository.get_by_category(category)
    return [format_product(p) for p in products]

def assign_category_to_product(product_id: str, category_id: str) -> dict:
    product = ProductRepository.get_by_id(product_id)
    if not product:
        raise NotFoundError(f"Product '{product_id}' not found.")
        
    category = ProductCategoryRepository.get_by_id(category_id)
    if not category:
        raise NotFoundError(f"Category '{category_id}' not found.")
        
    updated_product = ProductRepository.update(product, {"category": category})
    return format_product(updated_product)

def remove_category_from_product(product_id: str) -> dict:
    product = ProductRepository.get_by_id(product_id)
    if not product:
        raise NotFoundError(f"Product '{product_id}' not found.")
        
    updated_product = ProductRepository.update(product, {"category": None})
    return format_product(updated_product)

def bulk_create_products_from_csv(file_obj) -> dict:
    decoded_file = file_obj.read().decode('utf-8')
    io_string = io.StringIO(decoded_file)
    reader = csv.DictReader(io_string)
    
    created_count = 0
    errors = []
    
    for row_num, row in enumerate(reader, start=1):
        try:
            row['price'] = float(row.get('price', 0))
            row['quantity'] = int(row.get('quantity', 0))
            validate_product_data(row)
            ProductRepository.create(row)
            created_count += 1
            
        except Exception as e:
            errors.append(f"Row {row_num} failed: {str(e)}")
            
    return {
        "message": f"Successfully created {created_count} products.",
        "errors": errors
    }
