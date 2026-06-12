# EcoSplit Backend API 💸🌍

EcoSplit is a robust, production-ready Django REST Framework API designed to handle complex group expenses, live currency conversions, and optimized debt calculations for group travel.

Unlike basic CRUD applications, this project focuses heavily on **database optimization, data integrity, and system security**, showcasing advanced Django ORM techniques and custom middleware.

## 🚀 Key Engineering Features

* **Optimized Debt Calculation (Zero N+1 Queries):** Calculates complex "who owes whom" net balances for entire groups using a single database query via PostgreSQL-level math (`.annotate()`, `Coalesce`, and `Q` objects).
* **Financial Data Integrity:** Uses strict `Decimal` precision for all financial calculations to prevent floating-point rounding errors.
* **Transaction Safety:** Wraps complex multi-table database writes (creating an expense + generating multiple user splits) inside `transaction.atomic()` to guarantee database rollbacks if any step fails.
* **Custom Rate Limiting Middleware:** Implements a custom, cache-based middleware to throttle IP addresses (max 5 requests/minute) protecting the external currency API and database from spam.
* **Live Currency Conversion:** Integrates with the Fawazahmed0 Currency API to convert global currencies to the group's base currency in real-time, with historical date fallbacks for reliability.
* **Secure Authentication:** Endpoints are locked down using JSON Web Tokens (JWT) via `djangorestframework-simplejwt`.

## 🛠️ Tech Stack

* **Framework:** Django 5.x, Django REST Framework (DRF)
* **Database:** PostgreSQL / SQLite
* **Authentication:** JWT (JSON Web Tokens)
* **External APIs:** Fawazahmed0 Currency Exchange API
* **Core Python:** `decimal`, `requests`

## 🔀 Core API Endpoints

### Authentication
* `POST /api/login/` - Returns standard JWT Access and Refresh tokens.
* `POST /api/token/refresh/` - Refreshes the JWT Access token.

### Expenses
* `POST /api/expenses/` - Creates an expense, fetches live exchange rates, and automatically distributes the debt among group members. (Requires JWT)
  ```json
  // Request Payload Example
  {
      "group_id": 1,
      "amount": 100.00,
      "currency": "EUR",
      "splits": [
          {"user_id": 2, "amount": 50.00},
          {"user_id": 3, "amount": 50.00}
      ]
  }

## Group Balances

### Get Group Balances

**Endpoint**

```http
GET /api/groups/<group_id>/balances/
```

**Description**

Returns the fully optimized net balance for every member in the specified group.

**Net Balance Formula**

```text
Net Balance = Total Paid - Total Owed
```

A positive balance means the user is owed money, while a negative balance means the user owes money.

**Authentication**

Requires JWT Authentication.

**Example Request**

```http
GET /api/groups/1/balances/
Authorization: Bearer <access_token>
```

**Response Example**

```json
{
    "group_name": "Euro Trip 2026",
    "base_currency": "USD",
    "balances": [
        {
            "user_id": 1,
            "username": "alex",
            "net_balance": 150.50
        },
        {
            "user_id": 2,
            "username": "ben",
            "net_balance": -150.50
        }
    ]
}
```

**Response Fields**

| Field | Type | Description |
|---------|---------|-------------|
| group_name | string | Name of the group |
| base_currency | string | Group's default currency |
| balances | array | List of user balances |
| user_id | integer | User ID |
| username | string | Username |
| net_balance | decimal | User's net balance (Paid - Owed) |

---

# 💻 Local Setup & Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ecosplit-backend.git
cd ecosplit-backend
```

## 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
```

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 5. Create a Superuser

```bash
python manage.py createsuperuser
```

## 6. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```
