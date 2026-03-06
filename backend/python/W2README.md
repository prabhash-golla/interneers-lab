# 📦 Products API

A RESTful API for managing products with full CRUD support and pagination.

---

## Base URL

```
/api/v1/products/
```

---

## Endpoints

### 1. Create a Product

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

### 2. List Products

**`GET /api/v1/products/`**

Returns a paginated list of all products.

**Query Parameters:**

| Parameter | Type | Default | Description            |
|-----------|------|---------|------------------------|
| `page`    | int  | `1`     | Page number            |
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

### 3. Retrieve a Single Product

**`GET /api/v1/products/<product_id>/`**

Returns the details of a specific product.

**Response:** `200 OK`

**Error:** `404 Not Found` — product does not exist.

---

### 4. Update a Product

**`PUT /api/v1/products/<product_id>/`**

Replaces all fields of an existing product. All fields are required.

**Request Body** (JSON): Same structure as [Create a Product](#1-create-a-product).

**Response:** `200 OK`

**Errors:**
- `400 Bad Request` — validation failure
- `404 Not Found` — product does not exist

---

### 5. Delete a Product

**`DELETE /api/v1/products/<product_id>/`**

Permanently deletes a product.

**Response:** `200 OK`

**Error:** `404 Not Found` — product does not exist.

---

## Response Summary

| Method   | Endpoint                          | Success  | Errors              |
|----------|-----------------------------------|----------|---------------------|
| `POST`   | `/api/v1/products/`               | `201`    | —                   |
| `GET`    | `/api/v1/products/`               | `200`    | —                   |
| `GET`    | `/api/v1/products/<product_id>/`  | `200`    | `404`               |
| `PUT`    | `/api/v1/products/<product_id>/`  | `200`    | `400`, `404`        |
| `DELETE` | `/api/v1/products/<product_id>/`  | `200`    | `404`               |