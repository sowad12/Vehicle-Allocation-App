from fastapi import FastAPI
import uvicorn
from app.routers.allocationRoute import router as allocation_router
from app.routers.seederRoute import router as seeder_router

app = FastAPI()

app.include_router(allocation_router, prefix="/api/v1")
app.include_router(seeder_router, prefix="/api/v1")

#for debugging
if __name__=='__main__':
    uvicorn.run(app,host='0.0.0.0',port=8000)
 