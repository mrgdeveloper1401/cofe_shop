# Yadak Sadra Backend

A robust Django-based REST API for the **Yadak Sadra** automotive spare parts marketplace. This backend manages product catalogs, user authentication via OTP, shopping carts, and dynamic frontend layout configurations.

## 🚀 Key Features

### 🔐 Authentication & Users

  * **Phone-based Login:** Custom User model relies on phone numbers rather than emails.
  * **OTP Verification:** Secure login and registration using One-Time Passwords (OTP), handled asynchronously via **Celery**.
  * **JWT Support:** Uses `rest_framework_simplejwt` for secure, token-based authentication.

### 📦 Product Management

  * **Catalog Organization:** Manage Products, Brands, Countries of Origin, and Hierarchical Categories.
  * **Advanced Search:** Implements PostgreSQL's `SearchVector` for high-performance full-text search on product titles and descriptions.
  * **Filtering:** Filter products by brand, country, and price (cheap/expensive).

### 🛒 Shopping Cart

  * **Logic:** Add, remove, or decrease product counts in the user's cart.
  * **Auto-Calculation:** Uses Django Signals (`post_save`, `post_delete`) to automatically recalculate total cart prices whenever items change.

### 🎨 Dynamic Frontend Template

  * **Layout Control:** API endpoints to control home page sliders, banners, and footer links dynamically from the backend admin panel.

-----

## 🛠 Tech Stack

  * **Framework:** Django 5.2.7
  * **API:** Django Rest Framework (DRF)
  * **Database:** PostgreSQL (Required for full-text search features)
  * **Async Tasks:** Celery + Redis
  * **Documentation:** drf-yasg (Swagger/Redoc)

-----

## 📂 Project Structure

```
core/                   # Project settings and configuration
apps/
├── authentication/     # Login, Register, OTP logic
├── cart/               # Shopping cart models and API
├── product/            # Product catalog and Search API
├── template/           # Frontend layout configuration (Sliders, Footer)
user/                   # Custom User model definition
media/                  # User uploaded content
```

-----

## ⚙️ Installation

### 1\. Clone the repository

```bash
git clone https://github.com/merajpiri1383/yadak-sadra-backend.git
cd yadak-sadra-backend
```

### 2\. Set up Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3\. Environment Configuration

Create a `.env` file in the root directory (reference: `.env.example`):

```env
SECRET_KEY=your_secret_key_here
DEBUG=True
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
```

### 4\. Run Infrastructure (Redis)

Ensure Redis is running for Celery tasks:

```bash
redis-server
```

### 5\. Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6\. Run the Application

Open two terminal tabs:

**Terminal 1: Django Server**

```bash
python manage.py runserver
```

**Terminal 2: Celery Worker**

```bash
celery -A core worker -l info
```

-----

## 📖 API Documentation

The project includes auto-generated Swagger documentation. Once the server is running, visit:

  * **Swagger UI:** `http://127.0.0.1:8000/`
  * **Admin Panel:** `http://127.0.0.1:8000/admin/`