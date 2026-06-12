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
