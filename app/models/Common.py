from datetime import date, datetime
from pydantic import BaseModel,Field

class CommonModel(BaseModel):  
    id: int
    is_deleted: bool = False   
    updated_at: datetime = None 
    created_at: datetime = None