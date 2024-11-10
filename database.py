import os
from dotenv import load_dotenv
import motor.motor_asyncio
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

# Retrieve the MongoDB URI from environment variables
mongo_uri = os.getenv('MONGO_URI')

# Set up MongoDB client
client = MongoClient(mongo_uri)
db = client.chatbot
products_collection = db['products']

async def get_all_products():
    """Retrieve all products from the collection."""
    try:
        products = await products_collection.find().to_list(length=None)
        return products
    except Exception as e:
        print(f"Error while fetching products: {e}")
        return []