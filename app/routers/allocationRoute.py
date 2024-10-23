from fastapi import Depends, FastAPI,APIRouter, HTTPException
from app.query import * 
from app.service.allocationService import *

router = APIRouter()


@router.post("/create_allocations/",tags=["crud"])
async def create_allocation(allocation: AllocationCreate):
    return await create_allocation_service(allocation)

@router.put("/update_allocations/{allocation_id}",tags=["crud"])
async def update_allocation(allocation_id: str,allocation: AllocationUpdate):
    return await update_allocation_service(allocation_id,allocation)

@router.delete("/delete_allocations/{allocation_id}",tags=["crud"])
async def delete_allocation(allocation_id: str):
    return await delete_allocation_service(allocation_id)
  
@router.get("/get_allocation_history/",tags=["crud"])
async def get_allocation_history(allocation: AllocationGet = Depends()):
    return await fetch_allocation_history(allocation)  

@router.get("/get_all_drivers/",tags=["external"])
async def get_all_drivers():
    return await drivers_get()  

@router.get("/get_all_employees/",tags=["external"])
async def get_all_employees():
    return await employees_get()  

@router.get("/get_all_vehicles/",tags=["external"])
async def get_all_vehicles():
    return await vehicles_get()  


    