# 🛒 Order Service – Flask REST API (Enterprise Style)

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-black.svg)
![JWT](https://img.shields.io/badge/Auth-JWT-orange.svg)
![Swagger](https://img.shields.io/badge/API-Swagger-green.svg)
![MySQL](https://img.shields.io/badge/DB-MySQL-blue.svg)

---

## 📌 Project Overview

**Order Service** is a RESTful backend application built using **Flask**, following **enterprise-level architecture**.
It supports **authentication**, **order management**, **role-based access**, and **API documentation using Swagger (OpenAPI)**.

This project is designed to help **new developers** understand:

* How real backend services are structured
* How microservice-style APIs work
* How JWT authentication & roles are implemented

---

## 🧱 Tech Stack

| Layer          | Technology         |
| -------------- | ------------------ |
| Language       | Python             |
| Framework      | Flask              |
| Authentication | JWT                |
| Database       | MySQL              |
| ORM            | SQLAlchemy         |
| API Docs       | Swagger (Flasgger) |
| Tooling        | VS Code, Postman   |

---

## 📂 Project Structure

```
order-service/
│
├── app/
│   ├── controllers/      # API endpoints
│   ├── services/         # Business logic
│   ├── repositories/     # DB access layer
│   ├── models/           # DB models
│   ├── security/         # JWT & roles
│   ├── extensions/       # DB, JWT, Swagger
│   ├── config/           # Environment configs
│   └── main.py           # App entry point
│
├── requirements.txt
├── README.md
└── .env
```

---

## 🔐 Authentication Flow (JWT)

1️⃣ User **registers**
2️⃣ User **logs in** → receives **JWT token**
3️⃣ Token is sent in headers for protected APIs

```
Authorization: Bearer <JWT_TOKEN>
```

---

## 👥 Roles Supported

| Role  | Access               |
| ----- | -------------------- |
| USER  | Create / View Orders |
| ADMIN | View all orders      |

---

## 🚀 How to Run the Project (Step by Step)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/order-service.git
cd order-service
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

* **Windows**

```bash
venv\Scripts\activate
```

* **Linux / Mac**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment (`.env`)

```env
DB_URL=mysql+pymysql://user:password@localhost:3306/orderdb
JWT_SECRET_KEY=your-secret-key
```

---

### 5️⃣ Run the Application

```bash
python -m app.main
```

Server runs on:

```
http://127.0.0.1:5000
```

---

## 📘 Swagger API Documentation

Swagger UI:

```
http://127.0.0.1:5000/apidocs/
```

✔ View all APIs
✔ Test APIs directly
✔ Add JWT using **Authorize 🔐**

---

## 📬 Postman API Examples (For Beginners)

### 🔐 Register User

**POST** `/auth/register`

```json
{
  "username": "user1",
  "password": "pass123"
}
```

---

### 🔑 Login User

**POST** `/auth/login`

```json
{
  "username": "user1",
  "password": "pass123"
}
```

📥 Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 🛒 Create Order

**POST** `/orders`

Headers:

```
Authorization: Bearer <JWT_TOKEN>
```

Body:

```json
{
  "total_amount": 1200.50
}
```

---

### 📦 List Orders

**GET** `/orders`

Headers:

```
Authorization: Bearer <JWT_TOKEN>
```

---

### 👑 Admin – View All Orders

**GET** `/orders/admin/all`

Headers:

```
Authorization: Bearer <ADMIN_JWT_TOKEN>
```

---

## 🧠 Learning Outcomes (For Developers)

By completing this project, you will learn:

✅ Flask project structuring
✅ Controller–Service–Repository pattern
✅ JWT authentication
✅ Role-based authorization
✅ Swagger documentation
✅ Real-world API testing using Postman

---

## 🎯 Who Should Use This Project?

✔ Freshers / Students
✔ Backend learners
✔ Java → Python developers
✔ Interview preparation

---

## 📌 Future Enhancements

* Refresh tokens
* Docker support
* API Gateway integration
* Kubernetes deployment

---

## 🤝 Contributing

Pull requests are welcome.
Feel free to fork and improve this project.

---

## ⭐ If you find this useful

Give the repo a **star ⭐** and share it with others!

---

### 🧑‍💻 Author

**Abhisheik**
Building practical backend skills 🚀
