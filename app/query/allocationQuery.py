from datetime import date, datetime
from typing import Literal, Optional
from fastapi import Query
from pydantic import BaseModel, Field

class AllocationCreate(BaseModel):
    employee_id:int
    vehicle_id:int
    allocation_date:date


class AllocationUpdate(BaseModel):
    vehicle_id:int
    allocation_date:date    
    
class AllocationGet(BaseModel):
    employee_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at" 
    order_direction: Literal["asc", "desc"] = "asc"
    
  