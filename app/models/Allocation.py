from datetime import date, datetime
from pydantic import BaseModel,Field

class AllocationModel(BaseModel):
    employee_id: int
    vehicle_id: int
    allocation_date: datetime
    is_deleted: bool = False   
    updated_at: datetime = None 
    created_at: datetime = None
    
    
    

