from datetime import date, datetime
import logging
from bson import ObjectId
from fastapi import FastAPI,APIRouter, HTTPException
from app.models import *
from app.query import *
from app.config.dbconn import allocations_collection,employees_collection,vehicles_collection,drivers_collection


async def create_allocation_service(allocation: AllocationCreate):
   try:
    #check if vehicle exist in the vehicle collection
        vehicle_exists=await vehicles_collection.find_one({"id": allocation.vehicle_id})
        if not vehicle_exists:
            raise HTTPException(status_code=404, detail="invalid vehicle id.")
               
    #check if employee exist in the employee collection 
        employee_exists=await employees_collection.find_one({"id": allocation.employee_id})
        if not employee_exists:
            raise HTTPException(status_code=404, detail="invalid employee id.")
        
    #check if employee already allocated or not 
        employee_already_allocted= await allocations_collection.find_one({
                                                "employee_id": allocation.employee_id,
                                                "$expr": {
                                                    "$eq": [
                                                        {"$dateToString": {"format": "%Y-%m-%d", "date": "$allocation_date"}},
                                                        allocation.allocation_date.strftime('%Y-%m-%d')
                                                    ]
                                                }
                                            })
        
        if employee_already_allocted:
            raise HTTPException(status_code=404, detail="Employee already allocated for today.")
        
    # Check if the vehicle is already allocated for the specified date
        allocation_exists = await allocations_collection.find_one({
                                                "vehicle_id": allocation.vehicle_id,
                                                "$expr": {
                                                    "$eq": [
                                                        {"$dateToString": {"format": "%Y-%m-%d", "date": "$allocation_date"}},
                                                        allocation.allocation_date.strftime('%Y-%m-%d')
                                                    ]
                                                }
                                            })
        if allocation_exists:
            raise HTTPException(status_code=400, detail="Vehicle already allocated for this date.")
        
    # request payload data mapping
        allocation.allocation_date=datetime.combine(allocation.allocation_date, datetime.min.time())     
        allocation_model_data = AllocationModel(
            **allocation.dict(), 
            created_at=datetime.utcnow()       
        ).dict()
        
        result = await allocations_collection.insert_one(allocation_model_data)

        return {"allocation_id": str(result.inserted_id),"message":"successfully created."}
    
   except HTTPException as ex:   
      raise ex
          
   except Exception as e:          
        logging.error(f"Internal Server Error: {str(e)}")    
        raise HTTPException(status_code=500, detail="Internal server error.") 
    
async def update_allocation_service(allocation_id: str,allocation: AllocationUpdate):
   try:
    #check if vehicle exist in the vehicle collection        
        vehicle_exists=await vehicles_collection.find_one({"id": allocation.vehicle_id})
        if not vehicle_exists:
            raise HTTPException(status_code=404, detail="invalid vehicle id.")
              
    #Check valid allocation id                   
        get_allocation_data=await allocations_collection.find_one({"_id":ObjectId(allocation_id)})
        if not get_allocation_data:
            raise HTTPException(status_code=404, detail="allocation not found.")
        
    #Check if the vehicle is already allocated on this date or not         
        if get_allocation_data['vehicle_id']!=allocation.vehicle_id:
          is_vehicle_allocation=await allocations_collection.find_one({
                                                "vehicle_id": allocation.vehicle_id,
                                                "$expr": {
                                                    "$eq": [
                                                        {"$dateToString": {"format": "%Y-%m-%d", "date": "$allocation_date"}},
                                                        allocation.allocation_date.strftime('%Y-%m-%d')
                                                    ]
                                                }
                                            })                                                          
          if is_vehicle_allocation:
            raise HTTPException(status_code=404, detail="request vehicle already allocated for today.")  
           
    #cannot update past or current day allocation 
        if datetime.now().date() >= get_allocation_data['allocation_date'].date():
            raise HTTPException(status_code=400, detail="Cannot delete any past or current day allocation.")    
           
        allocation.allocation_date=datetime.combine(allocation.allocation_date, datetime.min.time())   
         
    #update data    
        updated_allocation = {
            "vehicle_id": allocation.vehicle_id,
            "allocation_date": allocation.allocation_date,
            "updated_at":datetime.utcnow()
         }
        await allocations_collection.update_one({"_id": ObjectId(allocation_id)}, {"$set": updated_allocation})
    
        return {"id": allocation_id,"message":"updated successfully"}   
    
   except HTTPException as ex:   
      raise ex
          
   except Exception as e:          
        logging.error(f"Internal Server Error: {str(e)}")    
        raise HTTPException(status_code=500, detail="Internal server error")     
    
async def delete_allocation_service(allocation_id: str):
        try:
          get_allocation_data=await allocations_collection.find_one({"_id":ObjectId(allocation_id)})
          if not get_allocation_data:
            raise HTTPException(status_code=404, detail="allocation not found")
        
        #cannot delete past or current day allocation 
          if datetime.now().date() >= get_allocation_data['allocation_date'].date():
            raise HTTPException(status_code=400, detail="Cannot delete any  past or current day allocation.")
        
          await allocations_collection.delete_one({"_id":ObjectId(allocation_id)})    
               
          return {"id": allocation_id,"message":"delete successfully"}   
       
        except HTTPException as ex:               
          raise ex        
        except Exception as e:          
            logging.error(f"Internal Server Error: {str(e)}")    
            raise HTTPException(status_code=500, detail="Internal server error")     
        
async def fetch_allocation_history(allocation: AllocationGet):        
        try:   
          
            query = {}    
            if allocation.employee_id:
                query["employee_id"] = allocation.employee_id
            if allocation.vehicle_id:
                query["vehicle_id"] = allocation.vehicle_id                
            
            sort_order = allocation.order_by if allocation.order_by in ["created_at", "updated_at"] else "created_at"
            direction = 1 if allocation.order_direction == "asc" else -1
                       
            allocations_data = await allocations_collection.find(query).sort(sort_order, direction).skip(allocation.offset).limit(allocation.limit).to_list(length=allocation.limit)
         
            result = []
            for val in allocations_data:
                result.append({
                    "_id": str(val["_id"]),                   
                    "employee_id": val["employee_id"],
                    "vehicle_id": val["vehicle_id"],              
                    "allocation_date": val["allocation_date"].strftime('%Y-%m-%d'),
                    "created_at": val["created_at"],
                    "updated_at": val["updated_at"]
                })
                
            res={
                "data": result,
                "limit": allocation.limit,
                "offset": allocation.offset,
                "total_results": len(allocations_data) 
             }            
            return res
        
        except HTTPException as ex:               
          raise ex        
        except Exception as e:          
            logging.error(f"Internal Server Error: {str(e)}")    
            raise HTTPException(status_code=500, detail="Internal server error")     
        
async def drivers_get():       
            try:
             drivers = await drivers_collection.find({}).to_list(length=None)
             
             if not drivers:
                raise HTTPException(status_code=404, detail="drivers not found")      
            
             for driver in drivers:
                  driver['_id'] = str(driver['_id'])     
                   
             return drivers
                     
            except HTTPException as ex:               
                raise ex        
            
            except Exception as e:          
                logging.error(f"Internal Server Error: {str(e)}")    
                raise HTTPException(status_code=500, detail="Internal server error")  
              
async def vehicles_get():       
            try:
             vehicles = await vehicles_collection.find({}).to_list(length=None)
             
             if not vehicles:
                raise HTTPException(status_code=404, detail="vehicles not found")      
            
             for vehicle in vehicles:
                  vehicle['_id'] = str(vehicle['_id'])     
                   
             return vehicles
                     
            except HTTPException as ex:               
                raise ex        
            
            except Exception as e:          
                logging.error(f"Internal Server Error: {str(e)}")    
                raise HTTPException(status_code=500, detail="Internal server error")                    

async def employees_get():       
            try:
             employees = await employees_collection.find({}).to_list(length=None)
             
             if not employees:
                raise HTTPException(status_code=404, detail="employees not found")      
            
             for employee in employees:
                  employee['_id'] = str(employee['_id'])     
                   
             return employees
                     
            except HTTPException as ex:               
                raise ex        
            
            except Exception as e:          
                logging.error(f"Internal Server Error: {str(e)}")    
                raise HTTPException(status_code=500, detail="Internal server error")                                