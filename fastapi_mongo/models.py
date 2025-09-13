from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class Employee(BaseModel):
    employee_id: str = Field(..., example="E123")
    name: str
    department: str
    salary: float
    joining_date: date
    skills: List[str]

class EmployeeUpdate(BaseModel):
    name: Optional[str]
    department: Optional[str]
    salary: Optional[float]
    joining_date: Optional[date]
    skills: Optional[List[str]]

class AvgSalaryResult(BaseModel):
    department: str
    avg_salary: float