# Finance Data Processing and Access Control Backend

## 📌 Overview

This project is a backend API for a Finance Dashboard system. It provides role-based access control, financial record management, and aggregated analytics for dashboard visualization.

The system supports multiple user roles with different permissions and provides endpoints for transaction management and summary analytics.

---

## 🚀 Features

### 1. User & Role Management

* Create users
* Assign roles (Admin, Analyst, Viewer)
* Manage user status (active/inactive)
* Role-based access control (RBAC)

### 2. Financial Records Management

* Create transactions
* View transactions
* Update transactions
* Delete transactions
* Filter transactions by:

  * Type (Income / Expense)
  * Category
  * Date

### 3. Dashboard Summary

* Total Income
* Total Expense
* Net Balance
* Category-wise totals
* Monthly summary
* Recent activity

### 4. Access Control

| Role    | Permissions                   |
| ------- | ----------------------------- |
| Viewer  | Read dashboard only           |
| Analyst | View records + analytics      |
| Admin   | Full access (users + records) |

### 5. Validation & Error Handling

* Input validation using Pydantic
* Proper HTTP status codes
* JWT authentication errors handled
* Role permission checks

---

## 🛠 Tech Stack

* FastAPI
* SQLAlchemy
* SQLite (default)
* JWT Authentication
* Pydantic
* Uvicorn

---

## 📂 Project Structure

```
app/
 ├── api/
 ├── core/
 ├── crud/
 ├── models/
 ├── schemas/
 ├── main.py
requirements.txt
README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```
git clone https://github.com/YOUR_USERNAME/finance-dashboard-api.git
cd finance-dashboard-api
```

### 2. Create Virtual Environment

```
python -m venv venv
```

Activate:

Windows:

```
venv\Scripts\activate
```

Mac/Linux:

```
source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

## ▶️ Running the Server

```
uvicorn app.main:app --reload
```

Server will start at:

```
http://localhost:8000
```

Swagger Documentation:

```
http://localhost:8000/docs
```

ReDoc:

```
http://localhost:8000/redoc
```

---

## 🔐 Authentication

Login to get JWT token:

```
POST /api/v1/login/access-token
```

Example:

```
curl -X POST "http://localhost:8000/api/v1/login/access-token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=admin@example.com&password=admin123"
```

Response:

```
{
  "access_token": "...",
  "token_type": "bearer"
}
```

Use token in header:

```
Authorization: Bearer <TOKEN>
```

---

## 👤 User Endpoints

### Create User

```
POST /api/v1/users/
```

Body:

```
{
  "email": "admin@test.com",
  "password": "admin123",
  "full_name": "Admin User",
  "role": "Admin"
}
```

---

### Get Current User

```
GET /api/v1/users/me
```

---

### Get All Users (Admin only)

```
GET /api/v1/users/
```

---

## 💰 Transaction Endpoints

### Create Transaction

```
POST /api/v1/transactions/
```

Body:

```
{
  "amount": 5000,
  "type": "Income",
  "category": "Salary",
  "notes": "Monthly salary"
}
```

---

### Get All Transactions

```
GET /api/v1/transactions/
```

---

### Filter by Type

```
GET /api/v1/transactions/?type=Expense
```

---

### Filter by Category

```
GET /api/v1/transactions/?category=Food
```

---

### Update Transaction

```
PUT /api/v1/transactions/{id}
```

---

### Delete Transaction

```
DELETE /api/v1/transactions/{id}
```

---

## 📊 Dashboard Endpoint

### Summary

```
GET /api/v1/dashboard/summary
```

Response Example:

```
{
  "total_income": 6500,
  "total_expense": 1000,
  "net_balance": 5500,
  "category_totals": {
    "Food": 850,
    "Salary": 6000
  },
  "monthly_summary": [],
  "recent_activity": []
}
```

---

## 🗄 Database

Default database:

```
SQLite (sql_app.db)
```

Automatically created on first run.

---

## 🔐 Role Based Access Control

| Endpoint            | Viewer | Analyst | Admin |
| ------------------- | ------ | ------- | ----- |
| View Dashboard      | ✅      | ✅       | ✅     |
| View Transactions   | ❌      | ✅       | ✅     |
| Create Transactions | ❌      | ❌       | ✅     |
| Delete Transactions | ❌      | ❌       | ✅     |
| Manage Users        | ❌      | ❌       | ✅     |

---

## 🧪 Example Test Flow

1. Create User
2. Login
3. Get Token
4. Create Transaction
5. Get Dashboard Summary

---

## 📦 Deployment (Render)

Start command:

```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## 📌 Assignment Requirements Mapping

| Requirement            | Implemented |
| ---------------------- | ----------- |
| User & Role Management | ✅           |
| Financial Records      | ✅           |
| Dashboard Summary      | ✅           |
| Access Control         | ✅           |
| Validation             | ✅           |
| Data Persistence       | ✅           |
| Filtering              | ✅           |
| Authentication         | ✅           |

---

## 👨‍💻 Author

Your Name

---

## 📄 License

This project is for assignment evaluation purposes.
