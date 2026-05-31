from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
import os

load_dotenv()

def connect_to_db():
    MONGO_URI = os.getenv('MONGO_URI')
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["microservices"]
    bucket = AsyncIOMotorGridFSBucket(db)
    return bucket