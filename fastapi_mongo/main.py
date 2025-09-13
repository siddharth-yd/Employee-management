from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import List, Optional

from .models import Employee, EmployeeUpdate, AvgSalaryResult
from . import crud, database
from .auth import create_access_token, get_current_user, fake_user, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI(title="Employee Assessment API")

@app.on_event("startup")
async def startup_db():
    await database.init_db()

# --- AUTH ---
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake_user["username"] or not verify_password(form_data.password, fake_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": form_data.username}, expires_delta=token_expires)
    return {"access_token": token, "token_type": "bearer"}

# --- PROTECTED CRUD ---
@app.post("/employees", response_model=dict)
async def create_employee(employee: Employee, user: dict = Depends(get_current_user)):
    return await crud.create_employee(employee.dict())

@app.put("/employees/{employee_id}", response_model=dict)
async def update_employee(employee_id: str, updates: EmployeeUpdate, user: dict = Depends(get_current_user)):
    return await crud.update_employee(employee_id, updates.dict(exclude_unset=True))

@app.delete("/employees/{employee_id}", response_model=dict)
async def delete_employee(employee_id: str, user: dict = Depends(get_current_user)):
    return await crud.delete_employee(employee_id)

# --- OPEN ROUTES ---
@app.get("/employees/{employee_id}", response_model=dict)
async def get_employee(employee_id: str):
    return await crud.get_employee(employee_id)

@app.get("/employees", response_model=List[dict])
async def list_employees(department: Optional[str] = None, limit: int = 10, skip: int = 0):
    if department:
        return await crud.list_employees_by_department(department)
    return await crud.list_employees(limit, skip)

@app.get("/employees/avg-salary", response_model=List[AvgSalaryResult])
async def avg_salary():
    return await crud.avg_salary_by_department()

@app.get("/employees/search", response_model=List[dict])
async def search(skill: str):
    return await crud.search_employees_by_skill(skill)