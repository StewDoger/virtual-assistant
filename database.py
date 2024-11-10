from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

client = MongoClient('mongodb://localhost:27017')
db = client['chatbot']
products_collection = db['products']

async def get_all_products():

    return await products_collection.find().to_list(length=None)