from datetime import date, datetime
import logging
from fastapi import FastAPI,APIRouter, HTTPException
from app.models import *
from app.query import *
from app.config.dbconn import employees_collection,vehicles_collection,drivers_collection
from bson import ObjectId

router = APIRouter()

@router.post("/seeder",tags=["external"])
async def seeder():
    try:
        total=0
        #employee seeder
        employee_data = [
            EmployeeModel(id=1,username="john_doe", email="john.doe@example.com",created_at=datetime.utcnow()),
            EmployeeModel(id=2,username="jane_smith", email="jane.smith@example.com",created_at=datetime.utcnow()),
            EmployeeModel(id=3,username="michael_brown", email="michael.brown@example.com",created_at=datetime.utcnow()),
            EmployeeModel(id=4,username="linda_jones", email="linda.jones@example.com",created_at=datetime.utcnow()),
            EmployeeModel(id=5,username="robert_wilson", email="robert.wilson@example.com",created_at=datetime.utcnow())
            ]
        
        existing_employee_ids = await employees_collection.distinct("id")

        # employees are already present
        employee_data_to_insert = []
        for employee in employee_data:
            if employee.id not in existing_employee_ids:
                employee_data_to_insert.append(employee.dict())

        if len(employee_data_to_insert) > 0:
            total+=len(employee_data_to_insert)
            await employees_collection.insert_many(employee_data_to_insert)
        
        #driver seeder
        driver_data = [
            DriverModel(id=1,name="robert",created_at=datetime.utcnow()),
            DriverModel(id=2,name="carlos",created_at=datetime.utcnow()),
            DriverModel(id=3,name="rahim",created_at=datetime.utcnow()),
            DriverModel(id=4,name="karim",created_at=datetime.utcnow()),
            DriverModel(id=5,name="umar",created_at=datetime.utcnow()),
            ]
        
        existing_driver_ids = await drivers_collection.distinct("id")
        
        driver_data_to_insert = []
        for driver in driver_data:
            if driver.id not in existing_driver_ids:
                driver_data_to_insert.append(driver.dict())
        
        if len(driver_data_to_insert) > 0:
            total+=len(driver_data_to_insert)
            await drivers_collection.insert_many(driver_data_to_insert)     

        #vehicle seeder
        vehicle_data = [
            VehicleModel(id=1,driver_id=2,created_at=datetime.utcnow()),
            VehicleModel(id=2,driver_id=1,created_at=datetime.utcnow()),
            VehicleModel(id=3,driver_id=3,created_at=datetime.utcnow()),
            VehicleModel(id=4,driver_id=4,created_at=datetime.utcnow()),
            VehicleModel(id=5,driver_id=5,created_at=datetime.utcnow()),
            ]
        
        existing_vehicle_ids = await vehicles_collection.distinct("id")
        
        vehicle_data_to_insert = []
        for vehicle in vehicle_data:
            if vehicle.id not in existing_vehicle_ids:
                vehicle_data_to_insert.append(vehicle.dict())
        
        if len(vehicle_data_to_insert) > 0:
            total+=len(vehicle_data_to_insert)
            await vehicles_collection.insert_many(vehicle_data_to_insert)     
          
        return {"status":str(total) +" data seeded sucessfully"}
    
    except Exception as e:   
        logging.error(f"Internal Server Error: {str(e)}")    
        raise HTTPException(status_code=500, detail="Internal server error")
