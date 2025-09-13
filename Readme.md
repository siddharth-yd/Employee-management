# FastAPI + MongoDB Employee Management

This is a complete Employee Management backend built using **FastAPI** and **MongoDB** with fully implemented **CRUD, Querying, Aggregation, Pagination, and JWT Authentication**.

---

## 🚀 Features
- Create, Read, Update, Delete Employees
- Unique validation on `employee_id`
- List employees by department (sorted by join date)
- Average salary aggregation by department
- Search employees by skill
- Pagination support
- MongoDB JSON Schema validation
- JWT Authentication (protect Create, Update, Delete)
  - username: `admin`
  - password: `admin123`

---

## ⚙️ Setup & Run

### 1. Clone repo
```bash
git clone https://github.com/siddharth-yd/Employee-management.git
cd fastapi_mongo
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
Note: Requires running MongoDB locally on default mongodb://localhost:27017

### 3. Start app
```bash
python -m uvicorn fastapi_mongo.main:app --reload
```
### 4. Access Docs
Open Swagger UI:
👉 http://127.0.0.1:8000/docs

🔑 Authentication
Get JWT token:

```bash
POST /token
username=admin
password=admin123
```
Use returned access_token in Authorize button at Swagger UI.

🧪 Example Endpoints
- POST /employees → Create employee (JWT required)
- GET /employees/{employee_id} → Fetch employee
- PUT /employees/{employee_id} → Update employee (JWT required)
- DELETE /employees/{employee_id} → Delete employee (JWT required)
- GET /employees?department=Engineering → Filter by department
- GET /employees/avg-salary → Aggregation
- GET /employees/search?skill=Python → Search employees by skill
- GET /employees?limit=5&skip=0 → Pagination