from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import dotenv_values,load_dotenv

load_dotenv()

# env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
# config = dotenv_values(env_path)
# uri=config.get("database_url")
uri = os.getenv("database_url")
# Create a new client and connect to the server 
client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))

db=client.allocation_system_db
employees_collection = db["employees"]
vehicles_collection = db["vehicles"]
drivers_collection = db["drivers"]
allocations_collection = db["allocations"]
counters_collection = db['counters']


# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


async def next_id(counter_name: str):
    counter = await counters_collection.find_one_and_update(
        {"_id": counter_name},
        {"$inc": {"sequence": 1}},
        return_document=True,
        upsert=True
    )
    return counter['sequence']
