from fastapi import HTTPException
from .database import employee_collection

def employee_helper(employee) -> dict:
    return {
        "id": str(employee["_id"]),
        "employee_id": employee["employee_id"],
        "name": employee["name"],
        "department": employee["department"],
        "salary": employee["salary"],
        "joining_date": employee["joining_date"],
        "skills": employee["skills"],
    }

# CREATE
async def create_employee(employee: dict) -> dict:
    existing = await employee_collection.find_one({"employee_id": employee["employee_id"]})
    if existing:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    result = await employee_collection.insert_one(employee)
    new_employee = await employee_collection.find_one({"_id": result.inserted_id})
    return employee_helper(new_employee)

# READ
async def get_employee(employee_id: str) -> dict:
    employee = await employee_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee_helper(employee)

# UPDATE
async def update_employee(employee_id: str, updates: dict) -> dict:
    employee = await employee_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    await employee_collection.update_one({"employee_id": employee_id}, {"$set": updates})
    updated_employee = await employee_collection.find_one({"employee_id": employee_id})
    return employee_helper(updated_employee)

# DELETE
async def delete_employee(employee_id: str) -> dict:
    result = await employee_collection.delete_one({"employee_id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}

# LIST by department
async def list_employees_by_department(department: str):
    employees = []
    cursor = employee_collection.find({"department": department}).sort("joining_date", -1)
    async for emp in cursor:
        employees.append(employee_helper(emp))
    return employees

# PAGINATED list
async def list_employees(limit: int = 10, skip: int = 0):
    employees = []
    cursor = employee_collection.find().skip(skip).limit(limit).sort("joining_date", -1)
    async for emp in cursor:
        employees.append(employee_helper(emp))
    return employees

# AVG salary
async def avg_salary_by_department():
    pipeline = [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}}
    ]
    results = await employee_collection.aggregate(pipeline).to_list(None)
    return [{"department": r["_id"], "avg_salary": round(r["avg_salary"], 2)} for r in results]

# SEARCH by skill
async def search_employees_by_skill(skill: str):
    employees = []
    cursor = employee_collection.find({"skills": skill})
    async for emp in cursor:
        employees.append(employee_helper(emp))
    return employees