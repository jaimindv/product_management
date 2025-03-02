# Build a Scalable Product Management API with DRF, PostgreSQL, Celery, and Redis

## Project Overview
This project is a RESTful API built using Django Rest Framework (DRF) with the following key features:

1. **Custom User Authentication** (Custom User Model, Login, Logout, Password Reset)
2. **Category & Product CRUD** (Admin Only)
3. **Dynamic Subcategories** (Tree Structure for Categories)
4. **Soft Delete Instead of Permanent Deletion**
5. **Bulk Upload of Products & Categories** from a JSON file (Processed in the background using Celery)

## Installation & Setup

### Technologies Used
- Python (v3.13.1)
- Django (v5.1.5)
- Django REST Framework v(3.15.2)
- PostgreSQL (v17.4)
- JWT Authentication


## Installation & Setup
1. Clone the repository:
   ```sh
   git clone <repo_url>
   cd <project_folder>
   ```
2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip insall -r requirements.txt
   ```
4. Apply migrations:
   ```sh
   python manage.py migrate
   ```
5. Run the development server:
   ```sh
   python manage.py runserver
   ```
---

## Features & Implementation Details

### 1. Authentication & User Management
- **Custom User Model** (Email-based authentication instead of username)
- **JWT Authentication** (using `djangorestframework-simplejwt`)
- **Endpoints:**
  - `POST /auth/register/` → Register a user
  - `POST /auth/login/` → Login
  - `POST /auth/logout/` → Logout (Blacklist token)
  - `PATCH /auth/update/` → Update user details
  - `POST /auth/forgot-password/` → Send password reset link via email

### 2. Category & Subcategory Management
- **Category Model** (Supports Dynamic Subcategories using a Parent-Child Relationship)
- **Admin CRUD Only**
- **Endpoints:**
  - `POST /category/` → Create category (Admin Only)
  - `GET /category/` → List all categories (Public)
  - `GET /category/{id}/` → Retrieve a specific category
  - `PATCH /category/{id}/` → Update category (Admin Only)
  - `DELETE /category/{id}/` → Soft delete category (Admin Only)

### 3. Product Management
- **Product Model** (Belongs to a Category)
- **CRUD only for Admin, Read for All Users**
- **Endpoints:**
  - `POST /product/` → Create a product (Admin Only)
  - `GET /product/` → List all products (Public)
  - `GET /product/{id}/` → Retrieve a specific product
  - `PATCH /product/{id}/` → Update product details (Admin Only)
  - `DELETE /product/{id}/` → Soft delete product (Admin Only)

### 4. Bulk Upload Categories & Products from JSON File (Using Celery)
- Users can upload a JSON file containing category and product data
- Processing is handled asynchronously using Celery to avoid request timeouts
- **Endpoints:**
  - `POST /upload/` → Upload JSON file for bulk processing

---


---

## License
This project is open-source.
