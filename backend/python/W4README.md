## Overview
This repository contains the backend service for an "AI-Powered Inventory Management System" built during the Interneers Lab 2026. 

As of **Week 4**, the project has evolved from a simple in-memory script to a robust, database-backed web service. It utilizes **Django** for the web framework but strictly adheres to a **Controller-Service-Repository (Hexagonal)** architecture. Data persistence is handled via **MongoDB** and the **MongoEngine** ORM, completely bypassing Django's default relational ORM to support flexible document-based storage.

## Architecture & Implementation
To ensure the application remains scalable, easily testable, and ready for AI integration, the codebase cleanly isolates concerns:

1. **Domain/Service Layer (`services.py`):** Contains pure Python business logic, input validation rules, and bulk processing scripts (like CSV uploads). It has no dependencies on Django web requests.
2. **Repository Layer (`repository.py`):** Acts as the bridge between the business logic and the database. It encapsulates all MongoEngine queries (`ProductRepository`, `ProductCategoryRepository`).
3. **Controller/Adapter Layer (`views.py`):** Acts as the interface between the web and the core logic. It extracts parameters/JSON/Files from HTTP requests and formats outputs into JSON responses.
4. **Data Models (`models.py`):** Defines the MongoDB document schemas, including relational references and automatic audit timestamps (`created_at`, `updated_at`).

### Features Developed (Weeks 1 - 4)
* **MongoDB Integration:** Full integration with a containerized MongoDB instance.
* **Relational Data Modeling:** `Product` documents now strictly reference `ProductCategory` documents.
* **Full CRUD APIs:** Endpoints to manage both products and product categories.
* **Bulk Processing:** API support for uploading a CSV file to create products in bulk.
* **Strict Data Validation:** Enforced business rules (e.g., preventing negative prices, ensuring `brand` is always provided).
* **Pagination:** The list APIs support `page` and `limit` query parameters for efficient data retrieval.
* **Meaningful Error Handling:** Custom exceptions map to appropriate HTTP status codes (400 Bad Request, 404 Not Found).

---

## Developer Guide

### Prerequisites
* **Python:** 3.12 or higher (3.14 recommended)
* **Docker & Docker Compose:** For running the local MongoDB instance.
* **Git:** For version control.

### Local Setup Instructions

1. **Create and activate a virtual environment:**
   ```bash
   cd backend/python
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the `backend/python` directory:
   ```
   MONGO_USER=root
   MONGO_PASS=example
   MONGO_PORT=27019
   MONGO_HOST=localhost
   ```

4. **Start the Database (Docker):**
   ```bash
   docker compose up -d
   ```

5. **Run the Development Server:**
   ```bash
   python manage.py runserver 8001
   ```

## API Reference

### Products API

Base URL: `/api/v1/products/`

---

#### 1. Create a Product

**`POST /api/v1/products/`**

Creates a new product.

**Request Body** (JSON):
```json
{
  "name": "Mechanical Keyboard",
  "description": "Tenkeyless mechanical keyboard.",
  "category": "Electronics",
  "price": 89.99,
  "brand": "KeyChron",
  "quantity": 45
}
```

| Field         | Type    | Description                    |
|---------------|---------|--------------------------------|
| `name`        | string  | Product name                   |
| `description` | string  | Short product description      |
| `category`    | string  | Product category               |
| `price`       | float   | Price of the product           |
| `brand`       | string  | Brand name                     |
| `quantity`    | integer | Stock quantity                 |

**Response:** `201 Created`

---

#### 2. List Products

**`GET /api/v1/products/`**

Returns a paginated list of all products.

**Query Parameters:**

| Parameter | Type | Default | Description              |
|-----------|------|---------|--------------------------|
| `page`    | int  | `1`     | Page number              |
| `limit`   | int  | `10`    | Number of items per page |

**Example Request:**
```
GET /api/v1/products/?page=1&limit=5
```

**Response:** `200 OK`
```json
{
  "items": [...],
  "total": 50,
  "page": 1,
  "limit": 5,
  "total_pages": 10
}
```

---

#### 3. Retrieve a Single Product

**`GET /api/v1/products/<product_id>/`**

Returns the details of a specific product.

**Response:** `200 OK`  
**Error:** `404 Not Found` — product does not exist.

---

#### 4. Update a Product

**`PUT /api/v1/products/<product_id>/`**

Replaces all fields of an existing product. All fields are required.

**Request Body** (JSON): Same structure as [Create a Product](#1-create-a-product).

**Response:** `200 OK`  
**Errors:**
- `400 Bad Request` — validation failure
- `404 Not Found` — product does not exist

---

#### 5. Delete a Product

**`DELETE /api/v1/products/<product_id>/`**

Permanently deletes a product.

**Response:** `200 OK`  
**Error:** `404 Not Found` — product does not exist.

---

#### 6. Bulk CSV Upload

**`POST /api/v1/products/bulk-upload/`**

Accepts a CSV file to create products in bulk.

**Request:** `multipart/form-data` with a `file` key.

**Response:** `200 OK`

---

#### Response Summary

| Method   | Endpoint                                | Success | Errors       |
|----------|-----------------------------------------|---------|--------------|
| `POST`   | `/api/v1/products/`                     | `201`   | —            |
| `GET`    | `/api/v1/products/`                     | `200`   | —            |
| `GET`    | `/api/v1/products/<product_id>/`        | `200`   | `404`        |
| `PUT`    | `/api/v1/products/<product_id>/`        | `200`   | `400`, `404` |
| `DELETE` | `/api/v1/products/<product_id>/`        | `200`   | `404`        |
| `POST`   | `/api/v1/products/bulk-upload/`         | `200`   | —            |

---

### Category APIs

* Create Category: `POST /api/v1/categories/`
* List Categories: `GET /api/v1/categories/`

### Relationship APIs

* Fetch Products by Category: `GET /api/v1/categories/<category_id>/products/`
* Assign Category to Product: `POST /api/v1/products/<product_id>/category/<category_id>/`
* Remove Category from Product: `DELETE /api/v1/products/<product_id>/category/`