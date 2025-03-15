# order-management


Used Stack: Python, Django, Django Rest Framework, PosgreSQL  

# Manual set up instructions: 
1. Clone repository: https://github.com/AibekMinbaev/order-management 
2. Create virtual env (recommended) 
3. Download packages from requirements.txt 
4. Set up the database 
    - change database configs in settings.py if you want to change the db (https://docs.djangoproject.com/en/5.1/ref/databases/)
    - if want to continue with PostgresSQL then 
    1. create database 
    2. create .env file for env variables and write following:  
    ```bash 
        DB_NAME=db_name 
        DB_USER=db_user
        DB_PASSWORD=password
        DB_HOST=localhost
        DB_PORT=5432
    ```
    3. note: can put credentials directly in settings.py, but using env variables is secure and good practice 
5. Make migrations & migrate   
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6. Run: 
    ```bash 
    python manage.py runserver
    ```

# API documentation, with implementatoin details: 

The base URL: 

```
http: http://localhost:8000/
```

## Authentication

This API uses JWT Bearer Token for authentication. You need to include the token in the `Authorization` header with the `Bearer` prefix for protected endpoints.

Example:

```
Authorization: Bearer YOUR_JWT_TOKEN
```

## Endpoints

### 1. **Products**

#### `GET /products/`

Fetch a paginated list of products.

**Response:**

- `200 OK`: Returns a list of products with pagination information.

Example Response:

```json
{
  "count": 100,
  "next": "http://localhost:8000/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Product 1",
      "description": "Description of product 1",
      "price": 10.99,
      "stock": 50
    },
    ...
  ]
}
```

#### `POST /products/`

Add a new product.

**Request Body:**

```json
{
  "name": "Product Name",
  "description": "Product Description",
  "price": 20.99,
  "stock": 100
}
```

**Response:**

- `201 Created`: Product successfully added.
- `400 Bad Request`: Invalid input.

#### `PATCH /products/{id}/`

Update product information.

**Parameters:**

- `id` (path parameter): The ID of the product to update.

**Request Body:**

```json
{
  "name": "Updated Product Name",
  "description": "Updated Product Description",
  "price": 19.99,
  "stock": 80
}
```

**Response:**

- `200 OK`: Product successfully updated.
- `404 Not Found`: Product not found.
- `400 Bad Request`: Invalid input.

---

### 2. **Promotions**

#### `GET /promotions/`

Fetch a paginated list of active promotions.

**Response:**

- `200 OK`: Returns a list of promotions with pagination information.

Example Response:

```json
{
  "count": 10,
  "next": "http://localhost:8000/promotions/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Promotion 1",
      "discount_type": "percentage",
      "value": 10,
      "start_date": "2025-01-01T00:00:00Z",
      "end_date": "2025-12-31T23:59:59Z"
    },
    ...
  ]
}
```

#### `POST /promotions/`

Add a new promotion.
- Validations: 
    - Start date is less then end date when adding, updating promotion

**Request Body:**

```json
{
  "name": "New Year Sale",
  "discount_type": "percentage",
  "value": 15,
  "start_date": "2025-01-01T00:00:00Z",
  "end_date": "2025-01-31T23:59:59Z"
}
```

**Response:**

- `201 Created`: Promotion successfully added.
- `400 Bad Request`: Invalid input.

#### `PATCH /promotions/{id}/`

Update promotion information.

**Parameters:**

- `id` (path parameter): The ID of the promotion to update.

**Request Body:**

```json
{
  "name": "Updated Promotion",
  "discount_type": "fixed",
  "value": 5,
  "start_date": "2025-01-01T00:00:00Z",
  "end_date": "2025-12-31T23:59:59Z"
}
```

**Response:**

- `200 OK`: Promotion successfully updated.
- `404 Not Found`: Promotion not found.
- `400 Bad Request`: Invalid input.

---

### 3. **Orders**

#### `POST /orders/`

Place an order, including calculating applicable discounts.

**Request Body:**

```json
{
  "user_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

**Response:**

- `201 Created`: Order successfully created.
- `400 Bad Request`: Invalid input or insufficient stock.

#### `GET /orders/`

Get a list of orders for the authenticated user.

**Response:**

- `200 OK`: Returns a list of orders for the authenticated user.

Example Response:

```json
{
  "count": 5,
  "next": "http://localhost:8000/orders/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user_id": 1,
      "total_price": 39.99,
      "status": "Pending",
      "items": [
        {
          "product_id": 1,
          "quantity": 2
        }
      ]
    },
    ...
  ]
}
```
